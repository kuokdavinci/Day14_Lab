import os
from engine.chunker import MarkdownLegalChunker
from engine.vector_store import QdrantStore
from engine.embedder import GoogleEmbedder
from tqdm import tqdm

def ingest_documents(source_dir: str):
    chunker = MarkdownLegalChunker(chunk_size=1000, chunk_overlap=150)
    store = QdrantStore()
    embedder = GoogleEmbedder()
    
    print(f"[*] Starting ingestion from {source_dir}...")
    store.reset() # Clean start for evaluation
    
    for filename in os.listdir(source_dir):
        if filename.endswith(".md"):
            with open(os.path.join(source_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()
                doc_metadata = {
                    "source_id": filename,
                    "title": filename.replace(".md", "").replace("_", " ").title()
                }
                chunks = chunker.chunk_document(doc_metadata, content)
                
                # Embedding in batches of 20
                batch_size = 20
                all_vectors = []
                print(f"  [+] Embedding {len(chunks)} chunks from {filename}...")
                for i in range(0, len(chunks), batch_size):
                    batch_texts = [c["content"] for c in chunks[i:i + batch_size]]
                    batch_vectors = embedder.embed_batch(batch_texts)
                    all_vectors.extend(batch_vectors)
                
                store.add_chunks(chunks, all_vectors)
                print(f"  [+] Ingested {len(chunks)} chunks from {filename}")

    print("✅ Ingestion complete!")

if __name__ == "__main__":
    ingest_documents("data/source")
