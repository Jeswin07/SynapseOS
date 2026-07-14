# Knowledge Graph Retrieval

# Introduction

Traditional Retrieval-Augmented Generation (RAG) systems rely primarily on semantic similarity to retrieve relevant information. While effective for concept matching, vector search alone may fail to capture explicit relationships between entities distributed across multiple documents or document sections.

To address this limitation, the Knowledge Intelligence module incorporates a Neo4j knowledge graph that represents relationships between documents, chunks, and extracted entities. Graph retrieval complements semantic retrieval by traversing these relationships to discover additional contextual information.

Rather than replacing vector retrieval, the knowledge graph acts as an additional retrieval signal that improves contextual completeness and supports multi-hop reasoning.

---

# Objectives

The graph retrieval component is designed to:

* Represent enterprise knowledge as a graph
* Connect related information across documents
* Enable entity-based retrieval
* Support multi-hop reasoning
* Expand retrieval context
* Improve answer completeness

---

# Why a Knowledge Graph?

Dense vector search retrieves information based on semantic similarity.

However, enterprise documents often contain relationships that are difficult to discover through embeddings alone.

Example:

```text
Customer
│
├── Places Order
│
├── Makes Payment
│
└── Requests Refund
```

These concepts may appear in different pages or entirely different documents.

A knowledge graph preserves these explicit relationships and allows the retrieval engine to navigate between them.

---

# Graph Architecture

```text
                 Document
                     │
             HAS_CHUNK
                     │
                     ▼
                  Chunk
                     │
          MENTIONED_IN
                     │
                     ▼
                  Entity
```

Each node stores structured metadata that can later be queried efficiently.

---

# Node Types

## Document

Represents an uploaded enterprise document.

Typical properties include:

* Document ID
* File Name
* File Type

A document acts as the parent node for all chunks extracted from that file.

---

## Chunk

Represents an individual text segment produced during document ingestion.

Typical properties include:

* Chunk ID
* Chunk Text
* Page Number
* Chunk Index
* Metadata

Chunks are the primary retrieval units used throughout the system.

---

## Entity

Represents meaningful concepts extracted from document text.

Examples include:

* Organizations
* Products
* Customers
* Locations
* Financial Terms
* Technical Concepts

Entities provide semantic connections across multiple documents.

---

# Relationships

The graph stores relationships between nodes to preserve document structure and semantic associations.

## HAS_CHUNK

```text
Document
     │
HAS_CHUNK
     ▼
Chunk
```

Connects a document with each of its chunks.

---

## MENTIONED_IN

```text
Entity
     │
MENTIONED_IN
     ▼
Chunk
```

Indicates that an entity appears within a particular chunk.

---

## NEXT_CHUNK

```text
Chunk A
     │
NEXT_CHUNK
     ▼
Chunk B
```

Preserves the original reading order of the document.

---

## PREVIOUS_CHUNK

```text
Chunk B
     │
PREVIOUS_CHUNK
     ▼
Chunk A
```

Allows navigation in the reverse direction.

Maintaining sequential relationships enables context expansion beyond a single retrieved chunk.

---

# Graph Construction

The knowledge graph is built during document ingestion.

Pipeline:

```text
Document

↓

Chunking

↓

Entity Extraction

↓

Create Document Node

↓

Create Chunk Nodes

↓

Create Entity Nodes

↓

Create Relationships

↓

Neo4j Graph
```

Graph construction occurs once during indexing and does not affect query latency.

---

# Query-Time Graph Retrieval

When a user submits a query, the graph retriever performs the following steps.

## Step 1

Extract entities from the user query.

Example:

```text
How are customer payments related to orders?
```

Entities:

* Customer
* Payment
* Order

---

## Step 2

Locate matching entity nodes inside Neo4j.

---

## Step 3

Retrieve chunks connected to those entities.

---

## Step 4

Expand context by traversing neighboring chunk relationships.

```text
Chunk

↓

NEXT_CHUNK

↓

NEXT_CHUNK

↓

NEXT_CHUNK
```

This captures surrounding information that may not have been returned by semantic retrieval alone.

---

## Step 5

Merge graph-derived chunks with results from hybrid retrieval.

Duplicate chunks are removed before reranking.

---

# Integration with Hybrid Retrieval

Graph retrieval operates alongside semantic retrieval rather than replacing it.

```text
                User Query
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
Hybrid Retrieval          Graph Retrieval
        │                         │
        └────────────┬────────────┘
                     ▼
          Candidate Context Pool
                     │
                     ▼
         Cross Encoder Reranker
                     │
                     ▼
             Final Context
```

The graph contributes additional evidence that may not be highly ranked by embedding similarity.

---

# Benefits

Adding graph retrieval provides several advantages.

## Better Context Expansion

Related chunks can be discovered even when they have low semantic similarity.

---

## Multi-Hop Reasoning

The graph enables traversal across multiple connected concepts.

Example:

```text
Customer

↓

Order

↓

Payment

↓

Invoice
```

This allows retrieval across chains of related information.

---

## Improved Recall

Relevant information connected through entities is less likely to be missed.

---

## Explainability

Relationships between retrieved chunks are explicit and inspectable within Neo4j.

This improves transparency compared with black-box embedding retrieval.

---

## Reduced Fragmentation

Neighboring chunks preserve document continuity, reducing the risk of answering questions using incomplete context.

---

# Current Limitations

The current implementation focuses on lightweight entity extraction and graph traversal.

Current limitations include:

* Rule-based entity extraction
* Limited relationship types
* No entity linking across external knowledge bases
* No graph embeddings
* No Graph Neural Networks (GNNs)

These choices keep indexing efficient while providing meaningful graph-enhanced retrieval.

---

# Future Enhancements

Potential improvements include:

* GraphRAG
* Automatic relationship extraction using LLMs
* Graph embeddings
* Community detection
* Knowledge graph summarization
* Graph-based reasoning agents
* Hybrid vector-graph ranking

---

# Summary

The knowledge graph complements dense retrieval by representing explicit relationships between enterprise concepts.

Instead of relying solely on semantic similarity, the retrieval engine combines:

* Dense vector retrieval
* BM25 keyword retrieval
* Graph traversal
* Cross-encoder reranking

This hybrid strategy improves contextual completeness, supports multi-hop reasoning, and provides a stronger foundation for grounded enterprise question answering.
