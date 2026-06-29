from src.ml.knowledge.graph.graph_retriever import GraphRetriever

retriever = GraphRetriever()

results = retriever.retrieve(
    "What does Article 39 prohibit?"
)

for chunk in results:

    print()

    print(chunk.payload["file_name"])

    print(chunk.payload["page_label"])

    print(chunk.payload["text"][:150])