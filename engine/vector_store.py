import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()

class QdrantStore:
    def __init__(self):
        self.host = os.getenv("QDRANT_HOST", "http://localhost:6333")
        self.collection_name = os.getenv("QDRANT_COLLECTION", "policy_docs_eval")
        self.client = QdrantClient(url=self.host)
        # Bám sát project cũ: dùng 768 chiều (thường cho Google Embedding)
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE", 768))

    def ensure_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            print(f"✅ Created collection: {self.collection_name}")

    def reset(self):
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass
        self.ensure_collection()

    def add_chunks(self, chunks, vectors):
        points = []
        for i, chunk in enumerate(chunks):
            points.append(PointStruct(
                id=chunk["id"],
                vector=vectors[i],
                payload={
                    "content": chunk["content"],
                    **chunk["metadata"]
                }
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_vector, query_text, limit=5):
        """
        Sử dụng Hybrid Search (RRF) tương tự project cũ
        """
        try:
            response = self.client.query_points(
                collection_name=self.collection_name,
                prefetch=[
                    # Nhánh 1: Semantic Search
                    models.Prefetch(query=query_vector, limit=limit * 2),
                    # Nhánh 2: Keyword Search trên nội dung
                    models.Prefetch(
                        filter=models.Filter(should=[
                            models.FieldCondition(key="content", match=models.MatchText(text=query_text))
                        ]),
                        query=None, 
                        limit=limit * 2
                    ),
                ],
                query=models.FusionQuery(fusion=models.Fusion.RRF),
                limit=limit
            )
            
            results = []
            for point in response.points:
                results.append({
                    "id": point.id,
                    "content": point.payload.get("content", ""),
                    "metadata": {k: v for k, v in point.payload.items() if k != "content"},
                    "score": point.score
                })
            return results
        except Exception as e:
            print(f"[-] Qdrant Search Error: {e}")
            return []
