"""Graph-based retriever using Neo4j."""

from __future__ import annotations

from src.ml.knowledge.graph.entity_extractor import EntityExtractor
from src.ml.knowledge.graph.neo4j_client import Neo4jClient
from src.ml.knowledge.retrieval_models import RetrievedChunk


class GraphRetriever:
    """
    Retrieves additional retrieval candidates from
    the Neo4j Knowledge Graph.

    Pipeline
    --------
    1. Extract entities from the query.
    2. Retrieve chunks mentioning those entities.
    3. Expand context using neighbouring chunks.
    4. Remove duplicate chunks.
    5. Return graph candidates for reranking.
    """

    def __init__(self) -> None:
        self.neo4j = Neo4jClient()
        self.extractor = EntityExtractor()

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[RetrievedChunk]:
        """
        Retrieve graph-based candidates.
        """

        entities = self.extractor.extract(query)

        if not entities:
            return []

        candidate_limit = max(top_k * 3, 20)

        cypher = """
        MATCH (e:Entity)
        WHERE e.name IN $entities

        MATCH (e)-[:MENTIONED_IN]->(c:Chunk)

        OPTIONAL MATCH (c)-[:NEXT_CHUNK]->(next:Chunk)
        OPTIONAL MATCH (c)-[:PREVIOUS_CHUNK]->(prev:Chunk)

        RETURN DISTINCT
            c,
            next,
            prev

        LIMIT $candidate_limit
        """

        rows = self.neo4j.execute(
            cypher,
            {
                "entities": entities,
                "candidate_limit": candidate_limit,
            },
        )

        seen: set[str] = set()

        results: list[RetrievedChunk] = []

        for row in rows:

            for key in (
                "c",
                "prev",
                "next",
            ):

                node = row[key]

                if node is None:
                    continue

                chunk_id = node["chunk_id"]

                if chunk_id in seen:
                    continue

                seen.add(chunk_id)

                score = 1.0 if key == "c" else 0.9

                payload = {
                    "chunk_id": chunk_id,
                    "text": node.get("text", ""),
                    "file_name": node.get("file_name", ""),
                    "page_label": node.get("page", ""),
                    "page_number": node.get("page"),
                }

                results.append(
                    RetrievedChunk(
                        payload=payload,
                        score=score,
                        graph_score=score,
                    )
                )

        return results[:top_k]

    def close(self) -> None:
        """Close Neo4j connection."""

        self.neo4j.close()