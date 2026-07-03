"""Client for the SynapseOS Knowledge API."""

from __future__ import annotations

import requests
from config import API_URL, TOP_K


class KnowledgeApiClient:
    """Simple client for the Knowledge Query API."""

    def __init__(self) -> None:
        self.url = API_URL

    def query(
        self,
        question: str,
    ) -> dict:
        """
        Query the running SynapseOS backend.
        """

        response = requests.post(
            self.url,
            json={
                "query": question,
                "collection_name": "enterprise_docs_v5",
                "top_k": TOP_K,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()