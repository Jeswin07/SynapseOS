"""Builds the enterprise knowledge graph."""

from __future__ import annotations

from src.ml.knowledge.graph.entity_extractor import EntityExtractor
from src.ml.knowledge.graph.neo4j_client import Neo4jClient


class GraphBuilder:
    """
    Builds the Neo4j knowledge graph
    from document chunks.
    """

    def __init__(self) -> None:

        self.neo4j = Neo4jClient()

        self.extractor = EntityExtractor()

        self.neo4j.create_constraints()

    def build(
        self,
        chunks: list[dict],
    ) -> None:
        """
        Build graph for one document.
        """

        previous_chunk = None

        for chunk in chunks:

            chunk_id = chunk["chunk_id"]

            text = chunk["text"]

            entities = self.extractor.extract(
                text,
            )

            # -----------------------
            # Create Chunk Node
            # -----------------------

            self.neo4j.execute(
                """
                MERGE (c:Chunk {chunk_id:$chunk_id})

                SET
                    c.text=$text,
                    c.file_name=$file_name,
                    c.page=$page
                """,
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "file_name": chunk["file_name"],
                    "page": chunk["page_label"],
                },
            )

            # -----------------------
            # Create Entity Nodes
            # -----------------------

            for entity in entities:

                self.neo4j.execute(
                    """
                    MERGE (e:Entity {name:$entity})

                    MERGE (c:Chunk {chunk_id:$chunk_id})

                    MERGE (e)-[:MENTIONED_IN]->(c)
                    """,
                    {
                        "entity": entity,
                        "chunk_id": chunk_id,
                    },
                )

            # -----------------------
            # Connect Consecutive Chunks
            # -----------------------

            if previous_chunk:

                self.neo4j.execute(
                    """
                    MATCH
                        (a:Chunk {chunk_id:$previous})

                    MATCH
                        (b:Chunk {chunk_id:$current})

                    MERGE
                        (a)-[:NEXT_CHUNK]->(b)
                    """,
                    {
                        "previous": previous_chunk,
                        "current": chunk_id,
                    },
                )

            previous_chunk = chunk_id

    def close(self) -> None:
        self.neo4j.close()