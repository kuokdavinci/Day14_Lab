import os
import asyncio
import time
from typing import List, Dict
from engine.retrieval_engine import LegalRetrievalEngine
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

class MainAgent:
    """
    Agent RAG thực tế kết nối với Qdrant và Jina Reranker.
    """
    def __init__(self, model: str = None):
        self.name = "SupportAgent-v1"
        self.retriever = LegalRetrievalEngine()
        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-4o-mini")

        # Chọn Prompt dựa trên biến môi trường (Mặc định là V2 - STRICT)
        self.mode = os.getenv("AGENT_MODE", "STRICT").upper()
        
        if self.mode == "HELPFUL":
            # Phiên bản V1: Nhiệt tình, hay suy luận
            self.system_prompt = """Bạn là một trợ lý ảo tư vấn về chính sách nội bộ.
            Hãy cố gắng trả lời câu hỏi của người dùng dựa trên Context. Nếu câu hỏi hơi mờ hồ, hãy cố gắng suy luận từ Context để hỗ trợ họ tốt nhất."""
        else:
            # Phiên bản V2: Khắt khe, an toàn
            self.system_prompt = """Bạn là một trợ lý ảo chuyên nghiệp tư vấn về chính sách nội bộ công ty.
            QUY TẮC NGHIÊM NGẶT (STRICT RULES):
            1. KIỂM TRA NGỮ CẢNH: Nếu câu hỏi mơ hồ hoặc không có thông tin khớp trong Context, hãy từ chối và yêu cầu làm rõ.
            2. TUYỆT ĐỐI KHÔNG SUY DIỄN: Không giả định thông tin không có trong Context.
            3. BẢO MẬT: Từ chối các yêu cầu vi phạm an ninh."""

    async def query(self, question: str) -> Dict:
        start_time = time.time()
        
        # 1. Retrieval (Hybrid Search + Jina Rerank)
        # Chúng ta chạy retrieve trong threadpool để không block async loop
        loop = asyncio.get_event_loop()
        retrieved_docs = await loop.run_in_executor(None, self.retriever.retrieve, question, 3)
        
        contexts = [doc["content"] for doc in retrieved_docs]
        context_str = "\n---\n".join(contexts)
        
        # 2. Generation (LLM)
        try:
            # Xác định API Key và Provider dựa trên model
            if "gemini" in self.model.lower():
                model_name = self.model.replace("gemini/", "")
                api_key = os.getenv("GOOGLE_API_KEY")
                provider = "gemini"
            elif "groq" in self.model.lower():
                model_name = self.model # LiteLLM dùng groq/llama...
                api_key = os.getenv("GROQ_API_KEY")
                provider = "groq"
            elif "qwen" in self.model.lower():
                model_name = self.model
                api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("DASH_SCOPE_API_KEY")
                provider = None # Dùng chuẩn OpenAI
                api_base = os.getenv("DASHSCOPE_API_BASE")
            else:
                model_name = self.model
                api_key = os.getenv("OPENAI_API_KEY")
                provider = None
                api_base = None

            response = completion(
                model=model_name,
                custom_llm_provider=provider,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {question}"}
                ],
                api_key=api_key,
                api_base=api_base,
                temperature=0
            )
            
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return {
                "answer": answer,
                "contexts": contexts,
                "retrieved_metadata": [doc["metadata"] for doc in retrieved_docs],
                "metadata": {
                    "model": self.model,
                    "tokens_used": tokens_used,
                    "latency_sec": round(time.time() - start_time, 2),
                    "sources": list(set([doc["metadata"].get("source_id", "Unknown") for doc in retrieved_docs]))
                }
            }
        except Exception as e:
            return {
                "answer": f"Đã có lỗi xảy ra: {str(e)}",
                "contexts": contexts,
                "retrieved_metadata": [doc["metadata"] for doc in retrieved_docs] if 'retrieved_docs' in locals() else [],
                "metadata": {"error": True}
            }

if __name__ == "__main__":
    agent = MainAgent()
    async def test():
        # Test 1: Thông thường
        print("\n--- Test 1: Fact Checking ---")
        resp = await agent.query("Mức phụ cấp lưu trú trong nước là bao nhiêu?")
        print(f"Answer: {resp['answer']}")
        
        # Test 2: Out of context
        print("\n--- Test 2: Out of Context ---")
        resp = await agent.query("Chính sách nghỉ thai sản như thế nào?")
        print(f"Answer: {resp['answer']}")

    asyncio.run(test())
