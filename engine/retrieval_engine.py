import os
import requests
from typing import List, Dict
from engine.vector_store import QdrantStore
from engine.embedder import GoogleEmbedder
from dotenv import load_dotenv

load_dotenv()

class LegalRetrievalEngine:
    def __init__(self):
        self.store = QdrantStore()
        self.embedder = GoogleEmbedder()
        self.jina_api_key = os.getenv("JINA_API_KEY")

    def retrieve(self, query: str, limit: int = 5, use_rerank: bool = False) -> List[Dict]:
        # 1. Embedding query
        query_vector = self.embedder.embed_query(query)

        # 2. Hybrid Search in Qdrant
        initial_results = self.store.search(query_vector, query, limit=limit)
        
        # Tạm tắt Jina Rerank để tránh lỗi kết nối
        return initial_results

if __name__ == "__main__":
    # Quick test
    engine = LegalRetrievalEngine()
    query = "Lương được trả vào ngày nào?"
    results = engine.retrieve(query)
    for i, res in enumerate(results):
        score = res.get("rerank_score", res.get("score", 0))
        print(f"[{i+1}] Score: {score:.4f} | {res['content'][:100]}...")
