# Retrieval Pipeline

# Introduction

The retrieval pipeline is responsible for identifying the most relevant information required to answer a user's question.

Instead of relying on a single retrieval technique, the Knowledge Intelligence module combines semantic vector search, keyword search, knowledge graph traversal, and neural reranking to maximize retrieval quality before answer generation.

This multi-stage retrieval architecture improves recall, ranking quality, contextual completeness, and factual grounding.

---

# Retrieval Overview

```text
                      User Question
                            │
                            ▼
                  Query Embedding Generation
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
     Dense Vector Search               BM25 Search
         (Qdrant)                    (Keyword Index)
            │                               │
            └───────────────┬───────────────┘
                            ▼
              Reciprocal Rank Fusion (RRF)
                            │
                            ▼
                  Knowledge Graph Expansion
                            │
                            ▼
                Cross Encoder Reranking
                            │
                            ▼
                    Top-K Context Chunks
                            │
                            ▼
                    Groq Answer Generator
```

---

# Step 1 — User Query

The retrieval process begins when a user submits a natural language question.

Example

```text
How are customer payments related to delivered orders?
```

The query is forwarded to the retrieval engine without any modification to preserve its original intent.

---

# Step 2 — Query Embedding

The user query is converted into a dense vector representation using the same embedding model employed during document ingestion.

The embedding captures the semantic meaning of the question rather than relying solely on keyword overlap.

Purpose

* Semantic similarity search
* Concept matching
* Retrieval of paraphrased content

---

# Step 3 — Dense Retrieval

The generated query embedding is used to search Qdrant.

Qdrant performs Approximate Nearest Neighbor (ANN) search to identify document chunks with embeddings closest to the query.

Advantages

* Semantic understanding
* Handles paraphrased queries
* Strong conceptual retrieval
* Fast vector search

Limitations

* May overlook exact keywords
* Sensitive to embedding quality
* Less effective for identifiers and codes

---

# Step 4 — BM25 Retrieval

In parallel, the query is executed against a BM25 index.

BM25 scores chunks using keyword frequency and document statistics.

Advantages

* Exact keyword matching
* Better retrieval of identifiers
* Better retrieval of legal references
* Better handling of product names
* Independent of embeddings

Limitations

* Limited semantic understanding
* Synonyms may not match
* Vocabulary mismatch

---

# Step 5 — Hybrid Retrieval

Dense retrieval and BM25 retrieval each have different strengths.

The module combines both result sets using Reciprocal Rank Fusion (RRF).

RRF assigns higher scores to documents that consistently rank well across multiple retrieval methods.

Benefits

* Higher recall
* Better robustness
* Reduced dependence on any single retrieval method
* More stable retrieval performance

The hybrid stage produces a larger candidate set than either retriever individually.

---

# Step 6 — Knowledge Graph Retrieval

The knowledge graph complements semantic retrieval by exploring explicit relationships stored in Neo4j.

The graph retriever performs the following operations:

1. Extract entities from the query.
2. Locate matching entities in Neo4j.
3. Retrieve related document chunks.
4. Retrieve neighboring chunks.
5. Remove duplicate results.
6. Merge graph candidates with hybrid retrieval.

This stage enables retrieval of context that may not be semantically similar but is structurally related.

Example

```text
Customer

↓

Order

↓

Payment

↓

Invoice
```

Even if these concepts are distributed across multiple chunks, graph traversal can connect them.

---

# Step 7 — Candidate Pool

After hybrid retrieval and graph expansion, the system builds a candidate pool containing all potentially relevant chunks.

The candidate pool intentionally prioritizes recall over precision.

At this stage, some lower-quality chunks may still be present.

The next stage is responsible for improving ranking quality.

---

# Step 8 — Cross Encoder Reranking

The Cross Encoder jointly evaluates each candidate chunk together with the original user query.

Unlike dense retrieval, the Cross Encoder does not compare independent embeddings.

Instead, it directly evaluates:

```text
(Query, Candidate Chunk)
```

This produces significantly more accurate relevance scores.

Benefits

* Better ranking accuracy
* Improved contextual relevance
* Stronger semantic understanding
* Reduced noisy retrieval

The highest-scoring chunks become the final retrieval context.

---

# Step 9 — Context Construction

The highest-ranked chunks are assembled into the final context supplied to the language model.

Each chunk retains its metadata, including:

* File name
* Page number
* Chunk identifier
* Similarity score

This allows generated answers to remain traceable to their original enterprise documents.

---

# Step 10 — Answer Generation

The final context is passed to the Groq language model.

The prompt instructs the model to:

* Answer only using retrieved context
* Avoid unsupported claims
* Produce concise and professional responses
* Ground every factual statement in retrieved evidence

This reduces hallucination and improves factual reliability.

---

# Retrieval Flow

```text
User Question
      │
      ▼
Embedding Generation
      │
      ▼
Dense Retrieval (Qdrant)
      │
      ├──────────────► BM25 Retrieval
      │
      ▼
Reciprocal Rank Fusion
      │
      ▼
Knowledge Graph Expansion
      │
      ▼
Cross Encoder Reranking
      │
      ▼
Top-K Context
      │
      ▼
Groq Generation
```

---

# Design Decisions

The retrieval architecture follows several guiding principles.

### Retrieval Before Generation

The language model never searches documents directly.

All retrieval is completed before answer generation.

---

### Multiple Retrieval Strategies

No single retrieval method performs well across every query type.

Combining dense search, keyword search, and graph traversal improves robustness.

---

### High Recall First

Early retrieval stages prioritize recall by collecting a broad candidate set.

Precision is improved later during reranking.

---

### Neural Reranking

Cross Encoder reranking significantly improves ranking quality compared with vector similarity alone.

Only the highest-quality chunks are forwarded to the language model.

---

### Explainability

Every retrieved chunk preserves its metadata, enabling generated answers to be traced back to the original source document.

---

# Advantages

Compared with a traditional vector-only RAG system, this pipeline provides:

* Improved retrieval recall
* Better ranking accuracy
* Stronger contextual grounding
* Better handling of keyword-heavy queries
* Multi-hop reasoning through graph traversal
* Reduced hallucination
* Enterprise-ready explainability

---

# Summary

The retrieval pipeline combines complementary retrieval techniques into a single workflow.

The overall process consists of:

1. Query embedding generation.
2. Dense vector retrieval.
3. BM25 keyword retrieval.
4. Reciprocal Rank Fusion.
5. Knowledge graph expansion.
6. Cross Encoder reranking.
7. Context construction.
8. Grounded answer generation.

This layered retrieval strategy provides higher-quality evidence to the language model and forms the foundation of the Knowledge Intelligence module.
