"""Neo4j client for the Knowledge Graph."""

from __future__ import annotations

from neo4j import GraphDatabase
from neo4j import Driver

from src.core.config import settings


class Neo4jClient:
    """
    Central Neo4j client.

    Responsible for:
    - Opening connections
    - Executing Cypher queries
    - Creating constraints
    """

    def __init__(self) -> None:

        self.driver: Driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
        )

    def close(self) -> None:
        """Close Neo4j connection."""

        self.driver.close()

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ):
        """
        Execute a Cypher query.
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                parameters or {},
            )

            return list(result)

    def create_constraints(self) -> None:
        """
        Create uniqueness constraints.
        """

        constraints = [

            """
            CREATE CONSTRAINT chunk_id
            IF NOT EXISTS
            FOR (c:Chunk)
            REQUIRE c.chunk_id IS UNIQUE
            """,

            """
            CREATE CONSTRAINT entity_name
            IF NOT EXISTS
            FOR (e:Entity)
            REQUIRE e.name IS UNIQUE
            """,
        ]

        for query in constraints:
            self.execute(query)