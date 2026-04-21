import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class GoogleEmbedder:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is missing in .env")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = os.getenv("GOOGLE_AI_MODEL", "text-embedding-004")
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", 768))

    def embed_text(self, text: str, task_type: str = "retrieval_document") -> list[float]:
        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.vector_size
                )
            )
            return response.embeddings[0].values
        except Exception as e:
            raise RuntimeError(f"Google Embedder Error: {e}")

    def embed_batch(self, texts: list[str], task_type: str = "retrieval_document") -> list[list[float]]:
        try:
            response = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.vector_size
                )
            )
            return [emb.values for emb in response.embeddings]
        except Exception as e:
            raise RuntimeError(f"Google Embedder Error for batch: {e}")

    def embed_query(self, text: str) -> list[float]:
        return self.embed_text(text, task_type="retrieval_query")
