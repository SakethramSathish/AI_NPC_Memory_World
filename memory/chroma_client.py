import chromadb
from chromadb.config import Settings
from typing import Optional
from config import CHROMA_DB_DIR
from models.embeddings import EmbeddingModel

class ChromaClient:
    """
    Centralized Chroma client.
    Responsible ONLY for DB + collection access
    """

    _client: Optional[chromadb.Client] = None

    @classmethod
    def get_client(cls) -> chromadb.Client:
        """
        Returns a singleton Chroma client.
        """
        if cls._client is None:
            cls._client = chromadb.Client(
                Settings(
                    persist_directory = str(CHROMA_DB_DIR),
                    anonymized_telemetry=False,
                )
            )
        return cls._client
    
    @classmethod
    def get_collection(cls, name: str):
        """
        Get or create a Chroma collection with explicit embeddings.
        """
        client = cls.get_client()

        # Adapter for ChromaDB's strict EmbeddingFunction signature
        # Expected: __call__(self, input: Documents) -> Embeddings
        class ChromaEmbeddingAdapter:
            def __call__(self, input: list[str]) -> list[list[float]]:
                # ChromaDB passes 'input' as a list of strings
                return EmbeddingModel.embed_texts(input)
            
            def name(self) -> str:
                return "ChromaEmbeddingAdapter"

        return client.get_or_create_collection(
            name=name,
            embedding_function=ChromaEmbeddingAdapter(),
        )

        return collection
    
    @classmethod
    def delete_collection(cls, name: str):
        """
        Utility function (mostly for testing).
        """
        client = cls.get_client()
        client.delete_collection(name)