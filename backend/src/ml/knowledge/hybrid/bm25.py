"""BM25 sparse retrieval engine."""

from __future__ import annotations

import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


class BM25Engine:
    """
    Persistent BM25 index.

    One index per collection.
    """

    INDEX_DIR = Path("artifacts/bm25")

    def __init__(self) -> None:

        self.INDEX_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def build_index(
        self,
        collection_name: str,
        chunks: list[str],
    ) -> None:
        """
        Build and persist BM25 index.
        """

        tokenized = [
            chunk.lower().split()
            for chunk in chunks
        ]

        bm25 = BM25Okapi(tokenized)

        data = {
            "bm25": bm25,
            "chunks": chunks,
        }

        with open(
            self._index_path(collection_name),
            "wb",
        ) as f:
            pickle.dump(data, f)

    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 10,
    ) -> list[dict]:

        path = self._index_path(collection_name)

        if not path.exists():
            return []

        with open(path, "rb") as f:
            data = pickle.load(f)

        bm25: BM25Okapi = data["bm25"]
        chunks: list[str] = data["chunks"]

        scores = bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for rank, (chunk, score) in enumerate(
            ranked[:top_k],
            start=1,
        ):
            results.append(
                {
                    "text": chunk,
                    "score": float(score),
                    "rank": rank,
                }
            )

        return results

    def _index_path(
        self,
        collection_name: str,
    ) -> Path:

        return (
            self.INDEX_DIR
            / f"{collection_name}.pkl"
        )