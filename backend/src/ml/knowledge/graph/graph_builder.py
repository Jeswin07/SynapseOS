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
        Build the graph for a single document.
        """

        if not chunks:
            return

        file_name = chunks[0]["file_name"]

        # -------------------------------------------------
        # Create Document node
        # -------------------------------------------------

        self.neo4j.execute(
            """
            MERGE (d:Document {name:$file_name})
            """,
            {
                "file_name": file_name,
            },
        )

        previous_chunk: str | None = None

        for chunk in chunks:

            chunk_id = chunk["chunk_id"]

            text = chunk["text"]

            entities = self.extractor.extract(text)

            # -------------------------------------------------
            # Chunk Node
            # -------------------------------------------------

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
                    "file_name": file_name,
                    "page": chunk["page_label"],
                },
            )

            # -------------------------------------------------
            # Document -> Chunk
            # -------------------------------------------------

            self.neo4j.execute(
                """
                MATCH (d:Document {name:$file_name})
                MATCH (c:Chunk {chunk_id:$chunk_id})

                MERGE (d)-[:HAS_CHUNK]->(c)
                """,
                {
                    "file_name": file_name,
                    "chunk_id": chunk_id,
                },
            )

            # -------------------------------------------------
            # Entity -> Chunk
            # -------------------------------------------------

            for entity in entities:

                self.neo4j.execute(
                    """
                    MERGE (e:Entity {name:$entity})

                    WITH e

                    MATCH (c:Chunk {chunk_id:$chunk_id})

                    MERGE (e)-[:MENTIONED_IN]->(c)
                    """,
                    {
                        "entity": entity,
                        "chunk_id": chunk_id,
                    },
                )

            # -------------------------------------------------
            # Chunk Relationships
            # -------------------------------------------------

            if previous_chunk is not None:

                self.neo4j.execute(
                    """
                    MATCH (a:Chunk {chunk_id:$previous})
                    MATCH (b:Chunk {chunk_id:$current})

                    MERGE (a)-[:NEXT_CHUNK]->(b)
                    MERGE (b)-[:PREVIOUS_CHUNK]->(a)
                    """,
                    {
                        "previous": previous_chunk,
                        "current": chunk_id,
                    },
                )

            previous_chunk = chunk_id

    def close(self) -> None:
        """Close Neo4j connection."""

        self.neo4j.close()