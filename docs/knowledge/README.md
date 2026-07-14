# Knowledge Intelligence Module

## Overview

The Knowledge Intelligence module is the enterprise Retrieval-Augmented Generation (RAG) engine of SynapseOS. It enables users to upload enterprise documents, retrieve relevant information using multiple retrieval strategies, and generate grounded responses using a Large Language Model (LLM).

Unlike a traditional semantic search system, this module combines multiple retrieval techniques—including dense vector retrieval, keyword search, knowledge graph retrieval, and cross-encoder reranking—to improve retrieval accuracy before answer generation.

The module is designed for enterprise document intelligence where factual correctness, explainability, and traceability are prioritized over open-domain generation.

---

# Objectives

The Knowledge module is designed to:

* Ingest enterprise documents
* Build semantic embeddings
* Store vector representations in Qdrant
* Build a Neo4j knowledge graph
* Retrieve information using hybrid search
* Improve ranking with a Cross Encoder
* Generate grounded answers using Groq LLM
* Evaluate retrieval and generation quality using benchmark datasets

---

# Key Features

## Document Processing

* PDF document ingestion
* Automatic document chunking
* Metadata extraction
* Embedding generation
* Vector storage

---

## Retrieval

* Dense semantic retrieval
* BM25 keyword retrieval
* Reciprocal Rank Fusion (RRF)
* Hybrid retrieval
* Knowledge graph retrieval
* Context expansion
* Cross-encoder reranking

---

## Generation

* Grounded answer generation
* Strict context-based prompting
* Source-aware responses
* Hallucination mitigation
* Structured enterprise responses

---

## Evaluation

### Retrieval Evaluation

* Precision@K
* Recall@K
* Hit Rate
* Mean Reciprocal Rank (MRR)
* Average Similarity
* Highest Similarity
* Retrieval Latency

### Generation Evaluation

* Faithfulness
* Answer Correctness
* Answer Relevancy
* Context Recall
* Semantic Similarity

---

# Technology Stack

| Component       | Technology                   |
| --------------- | ---------------------------- |
| Backend         | FastAPI                      |
| Vector Database | Qdrant                       |
| Graph Database  | Neo4j                        |
| Embedding Model | Sentence Transformers        |
| Keyword Search  | BM25                         |
| Hybrid Search   | Reciprocal Rank Fusion (RRF) |
| Reranker        | Cross Encoder                |
| LLM             | Groq                         |
| Evaluation      | Custom Benchmark Framework   |

---

# High-Level Architecture

```
Enterprise Documents
        │
        ▼
Document Loader
        │
        ▼
Chunking
        │
        ▼
Embedding Generation
        │
        ├──────────────► Qdrant
        │
        └──────────────► Neo4j Knowledge Graph
                               │
                               ▼
                     Hybrid Retrieval
              (Dense + BM25 + Graph)
                               │
                               ▼
                  Cross Encoder Reranker
                               │
                               ▼
                      Groq Answer Generator
                               │
                               ▼
                     Enterprise Response
```

---

# Module Structure

```
knowledge/

├── embeddings.py
├── retriever.py
├── hybrid_retriever.py
├── bm25.py
├── reranker.py
├── generator.py
├── llm_judge.py
├── semantic_similarity.py
├── generation_evaluator.py
│
├── graph/
│   ├── graph_builder.py
│   ├── graph_retriever.py
│   ├── entity_extractor.py
│   └── neo4j_client.py
│
├── evaluation/
│   ├── benchmark.py
│   ├── benchmark_loader.py
│   ├── evaluator.py
│   ├── metrics.py
│   └── generation/
│
└── loaders/
```

---

# Processing Pipeline

1. Upload enterprise documents.
2. Split documents into semantic chunks.
3. Generate embeddings.
4. Store vectors in Qdrant.
5. Build the Neo4j knowledge graph.
6. Execute hybrid retrieval (Dense + BM25).
7. Expand context using graph retrieval.
8. Rerank candidates using the Cross Encoder.
9. Generate grounded responses using Groq.
10. Evaluate retrieval and generation quality.

---

# Documentation

The following documents provide detailed explanations of each component.

| Document              | Description                                 |
| --------------------- | ------------------------------------------- |
| overview.md           | Module overview and design goals            |
| architecture.md       | System architecture                         |
| ingestion_pipeline.md | Document ingestion workflow                 |
| retrieval_pipeline.md | Hybrid retrieval pipeline                   |
| graph_retrieval.md    | Knowledge graph design                      |
| reranking.md          | Cross Encoder reranking                     |
| evaluation.md         | Benchmarking and evaluation                 |
| api.md                | API documentation                           |
| configuration.md      | Environment variables                       |
| limitations.md        | Current limitations and future improvements |

---

# Current Capabilities

* Enterprise document intelligence
* Hybrid Retrieval-Augmented Generation (RAG)
* Knowledge graph-enhanced retrieval
* Cross-encoder reranking
* Benchmark-driven evaluation
* Production-oriented modular architecture
* GraphRAG

---

# Future Enhancements

* Multimodal document support
* Incremental graph updates
* Multi-document summarization
* Agentic retrieval workflows
* Streaming responses
* Multi-language support
