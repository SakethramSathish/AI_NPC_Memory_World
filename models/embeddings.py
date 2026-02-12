from sentence_transformers import SentenceTransformer
from typing import List
from config import EMBEDDING_MODEL_NAME

class EmbeddingModel:
    """
    Singleton-style embedding wrapper to ensure
    the SAME embedding model is used everywhere.
    """

    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return cls._model
    
    @classmethod
    def embed_text(cls, text: str) -> List[float]:
        """
        Embed a single string into a vector.
        """
        model = cls.load_model()
        return model.encode(text).tolist()

    @classmethod
    def embed_texts(cls, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple strings into vectors.
        """
        model = cls.load_model()
        return model.encode(texts).tolist()