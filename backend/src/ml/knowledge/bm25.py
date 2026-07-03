"""BM25 keyword retriever for Hybrid RAG."""

from __future__ import annotations

import re

import nltk
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Lightweight BM25 retriever over indexed document chunks."""

    def __init__(self) -> None:
        self._bm25: BM25Okapi | None = None
        self._documents: list[dict] = []

    @property
    def ready(self) -> bool:
        """Returns True if the BM25 index has been built."""
        return self._bm25 is not None

    def build(
        self,
        documents: list[dict],
    ) -> None:
        """
        Build the BM25 index.

        Each document should contain at least:
        {
            "text": "...",
            "payload": {...}
        }
        """
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")

        self._documents = documents

        corpus = [
            self._tokenize(
                document["text"]
            )
            for document in documents
        ]

        self._bm25 = BM25Okapi(corpus)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Returns the top BM25 documents.
        """

        if self._bm25 is None:
            return []

        query_tokens = self._tokenize(query)

        scores = self._bm25.get_scores(query_tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )

        results: list[dict] = []

        for index, score in ranked[:top_k]:

            document = self._documents[index].copy()

            document["bm25_score"] = float(score)

            results.append(document)

        return results
    
    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:
        """
        Normalize text before BM25 indexing.
        """

        text = text.lower()

        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
        )

        return word_tokenize(text)