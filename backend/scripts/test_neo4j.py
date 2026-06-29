from src.ml.knowledge.graph.neo4j_client import Neo4jClient

client = Neo4jClient()

client.create_constraints()

print("Neo4j connected successfully!")

client.close()