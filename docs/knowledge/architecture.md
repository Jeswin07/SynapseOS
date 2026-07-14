# Knowledge Module Architecture

# Introduction

The Knowledge Intelligence module implements a production-oriented Retrieval-Augmented Generation (RAG) architecture for enterprise document intelligence.

Instead of relying solely on semantic vector search, the system combines multiple retrieval techniques, knowledge graph expansion, and neural reranking to maximize retrieval quality before passing the retrieved context to the Large Language Model (LLM).

The architecture is modular, allowing each stage of the retrieval pipeline to be independently improved or replaced without affecting the remaining components.

---

# Architecture Overview

```text
                    Enterprise Documents
                             │
                             ▼
                    Document Loader
                             │
                             ▼
                  Chunking & Metadata
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   Embedding Generation             Entity Extraction
            │                                 │
            ▼                                 ▼
        Qdrant Vector DB                Neo4j Graph
            │                                 │
            └──────────────┬──────────────────┘
                           ▼
                   Hybrid Retrieval
                (Dense + BM25 + Graph)
                           │
                           ▼
                Cross Encoder Reranker
                           │
                           ▼
                 Context Construction
                           │
                           ▼
                  Groq LLM Generation
                           │
                           ▼
                  Enterprise Response
```

---

# System Components

## 1. Document Loader

The document loader is responsible for reading uploaded enterprise documents and extracting raw textual content.

Responsibilities:

* Read supported document formats
* Preserve page information
* Preserve document metadata
* Prepare raw text for chunking

Output:

* Raw document text
* Metadata
* Page information

---

## 2. Chunking Pipeline

Large documents cannot be embedded directly.

The chunking pipeline divides documents into manageable semantic chunks while preserving context.

Each chunk contains:

* chunk_id
* file_name
* page_number
* page_label
* text
* chunk_index
* metadata

These chunks become the fundamental retrieval units throughout the system.

---

## 3. Embedding Generation

Each document chunk is converted into a dense vector representation using a Sentence Transformer embedding model.

Purpose:

* Capture semantic meaning
* Enable similarity search
* Support vector retrieval

Generated embeddings are stored inside Qdrant.

---

## 4. Vector Database (Qdrant)

Qdrant stores dense vector embeddings together with document metadata.

Stored information includes:

* embedding vector
* chunk text
* file name
* page label
* chunk identifier
* additional metadata

Qdrant performs Approximate Nearest Neighbor (ANN) search to retrieve semantically similar chunks.

---

## 5. BM25 Index

Semantic retrieval performs well for conceptual similarity but may overlook exact keywords.

To improve retrieval robustness, the module builds a BM25 index over all document chunks.

Advantages:

* Exact keyword matching
* Better retrieval for identifiers
* Better retrieval for legal references
* Improved handling of domain-specific terminology

---

## 6. Hybrid Retrieval

The system combines:

* Dense Retrieval
* BM25 Retrieval

using Reciprocal Rank Fusion (RRF).

Advantages:

* Better recall
* Better robustness
* Reduced dependence on embedding quality
* Improved performance across document types

Hybrid retrieval produces a larger candidate set for later reranking.

---

## 7. Knowledge Graph

A Neo4j knowledge graph is constructed during document ingestion.

Node Types:

* Document
* Chunk
* Entity

Relationships:

* HAS_CHUNK
* MENTIONED_IN
* NEXT_CHUNK
* PREVIOUS_CHUNK

The graph enables structural navigation beyond semantic similarity.

---

## 8. Graph Retrieval

The graph retriever expands retrieved context by traversing entity relationships.

Pipeline:

1. Extract entities from the user query.
2. Locate matching entities.
3. Retrieve related chunks.
4. Retrieve neighboring chunks.
5. Remove duplicates.
6. Return graph candidates.

Graph retrieval improves multi-hop reasoning and contextual completeness.

---

## 9. Cross Encoder Reranker

Hybrid retrieval prioritizes recall over ranking accuracy.

A Cross Encoder evaluates each candidate together with the original query.

Instead of independently embedding documents and queries, the Cross Encoder jointly evaluates:

(Query, Chunk)

This produces significantly better ranking quality than vector similarity alone.

Only the highest-ranked chunks are forwarded to the language model.

---

## 10. Answer Generation

The Groq LLM generates the final response using only the retrieved context.

The generation prompt enforces:

* No external knowledge
* No hallucination
* Context-grounded answers
* Professional formatting
* Source-aware responses

The model synthesizes information from multiple retrieved chunks into a single enterprise response.

---

# Retrieval Pipeline

```text
User Query
      │
      ▼
Embedding Generation
      │
      ▼
Dense Retrieval (Qdrant)
      │
      ├─────────────► BM25 Retrieval
      │
      ├─────────────► Graph Retrieval
      │
      ▼
Reciprocal Rank Fusion
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Top-K Context
      │
      ▼
Groq Generator
      │
      ▼
Answer
```

---

# Design Principles

The architecture follows several guiding principles:

* Modular components
* Retrieval before generation
* Grounded responses
* Explainable retrieval
* Extensible architecture
* Production-oriented design
* Benchmark-driven evaluation

Each component has a single responsibility, making the system easier to maintain, test, and extend.

---

# Benefits of the Architecture

Compared with a traditional semantic search system, this architecture provides:

* Improved retrieval recall
* Better ranking accuracy
* Reduced hallucination
* Stronger contextual grounding
* Multi-hop document reasoning
* Enterprise-ready scalability
* Comprehensive evaluation support

These characteristics make the Knowledge Intelligence module suitable for enterprise decision intelligence scenarios where retrieval quality and factual correctness are critical.
