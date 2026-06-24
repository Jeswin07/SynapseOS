"""Handles document chunking and local vector embedding generation."""

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    """Singleton engine for generating embeddings and chunking documents."""

    _instance = None
    _model = None

    def __new__(cls) -> "EmbeddingEngine":
        """Ensures the heavy embedding model is only loaded into memory once."""
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)
            
            print("Loading local embedding model: BAAI/bge-small-en-v1.5...")
            cls._instance._model = SentenceTransformer("BAAI/bge-small-en-v1.5")
            
            cls._instance._splitter = SentenceSplitter(
                chunk_size=512,
                chunk_overlap=50,
            )
        return cls._instance

    def chunk_document(self, file_path: str, metadata: dict | None = None) -> list:
        """Parses a file (PDF, TXT, CSV) into semantic nodes via LlamaIndex."""
        # SimpleDirectoryReader handles the format extraction automatically
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        
        # Inject our custom metadata (like document_id) into LlamaIndex docs
        if metadata:
            for doc in documents:
                doc.metadata.update(metadata)
                
        nodes = self._splitter.get_nodes_from_documents(documents)
        return nodes

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Converts a list of text strings into dense numerical vectors."""
        if not texts:
            return []

        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()