import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import faiss
import numpy as np
from app.config import settings

class VectorDBService:
    def __init__(self):
        self.db_type = settings.VECTOR_DB_TYPE
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        if self.db_type == "chromadb":
            self.client = chromadb.PersistentClient(
                path=settings.VECTOR_DB_PATH,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name="donor_emails",
                metadata={"description": "Donor email embeddings"}
            )
        elif self.db_type == "faiss":
            self.dimension = 384  # all-MiniLM-L6-v2 dimension
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata_store = {}
    
    def add_email(self, email_id: str, content: str, metadata: Dict):
        """Add email to vector database"""
        embedding = self.embedding_model.encode(content)
        
        if self.db_type == "chromadb":
            self.collection.add(
                ids=[email_id],
                embeddings=[embedding.tolist()],
                metadatas=[metadata],
                documents=[content]
            )
        elif self.db_type == "faiss":
            self.index.add(np.array([embedding]))
            self.metadata_store[email_id] = {
                "content": content,
                **metadata
            }
    
    def search_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for similar emails"""
        query_embedding = self.embedding_model.encode(query)
        
        if self.db_type == "chromadb":
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            return [
                {
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                }
                for i in range(len(results['ids'][0]))
            ]
        elif self.db_type == "faiss":
            distances, indices = self.index.search(
                np.array([query_embedding]), top_k
            )
            return [
                {
                    "id": list(self.metadata_store.keys())[idx],
                    "content": self.metadata_store[list(self.metadata_store.keys())[idx]]["content"],
                    "distance": float(distances[0][i])
                }
                for i, idx in enumerate(indices[0])
            ]
    
    def get_all_emails(self) -> List[Dict]:
        """Retrieve all stored emails"""
        if self.db_type == "chromadb":
            results = self.collection.get()
            return [
                {
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i]
                }
                for i in range(len(results['ids']))
            ]
        elif self.db_type == "faiss":
            return list(self.metadata_store.values())

vector_db = VectorDBService()