"""Enterprise embedding engine."""

from __future__ import annotations

from typing import Any

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from sentence_transformers import SentenceTransformer

from src.core.config import settings
from src.ml.knowledge.loaders import DocumentLoader
from src.shared.logging import logger


class EmbeddingEngine:
    """
    Enterprise embedding engine.

    Responsibilities
    ----------------
    - Load embedding model once
    - Load documents
    - Chunk documents
    - Generate embeddings
    """

    _instance: EmbeddingEngine | None = None

    _model: SentenceTransformer
    _splitter: SentenceSplitter
    _loader: DocumentLoader

    def __new__(cls) -> EmbeddingEngine:

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            logger.info(
                "Loading embedding model '%s'.",
                settings.embedding_model,
            )

            cls._instance._model = SentenceTransformer(
                settings.embedding_model
            )

            cls._instance._splitter = SentenceSplitter(
                chunk_size=settings.knowledge_chunk_size,
                chunk_overlap=settings.knowledge_chunk_overlap,
                separator="\n",
                paragraph_separator="\n\n",
            )

            cls._instance._loader = DocumentLoader()

        return cls._instance

    def chunk_document(
        self,
        file_path: str,
        metadata: dict[str, Any] | None = None,
    ) -> list:
        """
        Load a document and split it into semantic chunks.
        """

        loaded_documents = self._loader.load(file_path)

        documents: list[Document] = []

        for item in loaded_documents:

            doc_metadata = {}

            if metadata:
                doc_metadata.update(metadata)

            doc_metadata["page_label"] = item["page_label"]

            documents.append(
                Document(
                    text=item["text"],
                    metadata=doc_metadata,
                )
            )

        nodes = self._splitter.get_nodes_from_documents(
            documents
        )

        return nodes

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate normalized embeddings.
        """

        if not texts:
            return []

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embedding for one text.
        """

        return self.generate_embeddings(
            [text]
        )[0]

    @property
    def embedding_dimension(self) -> int:
        return self._model.get_sentence_embedding_dimension()

    @property
    def model_name(self) -> str:
        return self.MODEL_NAME