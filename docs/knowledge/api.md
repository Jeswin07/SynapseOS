# Knowledge Module API

# Introduction

The Knowledge Intelligence module exposes REST APIs for document ingestion and enterprise knowledge retrieval.

These APIs provide the interface between the frontend application and the Knowledge Intelligence pipeline, allowing users to upload enterprise documents and query indexed knowledge using Retrieval-Augmented Generation (RAG).

All API responses are returned in JSON format.

---

# API Overview

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/knowledge/upload` | POST | Upload and index enterprise documents |
| `/knowledge/query` | POST | Query the enterprise knowledge base |

---

# Document Upload API

## Endpoint

```http
POST /knowledge/upload
```

---

## Description

Uploads an enterprise document, extracts text, generates embeddings, builds the knowledge graph, and indexes the document for future retrieval.

---

## Request

```http
Content-Type: multipart/form-data
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Enterprise document to ingest |

---

## Example Request

```bash
curl -X POST \
  http://localhost:8000/knowledge/upload \
  -F "file=@enterprise_document.pdf"
```

---

## Successful Response

```json
{
    "message": "Document ingested successfully.",
    "document_id": "6cf2d4e5",
    "chunks_processed": 218,
    "collection_name": "enterprise_docs_v5"
}
```

---

# Upload Processing Pipeline

```text
Document Upload
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
 ┌─────┴─────┐
 ▼           ▼
Qdrant     Neo4j
       │
       ▼
Response
```

---

# Knowledge Query API

## Endpoint

```http
POST /knowledge/query
```

---

## Description

Retrieves relevant enterprise knowledge using hybrid retrieval, graph retrieval, and cross-encoder reranking before generating a grounded response using the configured LLM.

---

## Request Body

```json
{
    "query": "How are customer payments related to delivered orders?",
    "collection_name": "enterprise_docs_v5",
    "top_k": 5
}
```

---

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | User question |
| collection_name | string | No | Target knowledge collection |
| top_k | integer | No | Number of chunks retrieved before reranking |

---

## Successful Response

```json
{
    "answer": "Customer payments are linked to delivered orders using the order_id field.",

    "sources": [
        {
            "text": "...",
            "score": 0.94,
            "file_name": "olist_orders_dataset.pdf",
            "page_label": "12",
            "page_number": 12,
            "chunk_index": 4,
            "chunk_length": 486,
            "chunk_id": "chunk_124"
        }
    ],

    "metrics": {
        "retrieval_time_ms": 62.4,
        "generation_time_ms": 418.6,
        "total_time_ms": 481.0,
        "chunks_retrieved": 5,
        "average_similarity": 0.82,
        "highest_similarity": 0.94
    }
}
```

---

# Query Processing Pipeline

```text
User Query
      │
      ▼
Query Embedding
      │
      ▼
Dense Retrieval (Qdrant)
      │
      ├────────────► BM25 Retrieval
      │
      ├────────────► Graph Retrieval
      │
      ▼
Reciprocal Rank Fusion (RRF)
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Top-K Context
      │
      ▼
Groq LLM
      │
      ▼
Generated Response
```

---

# Response Models

## QueryResponse

| Field | Type | Description |
|--------|------|-------------|
| answer | string | Generated answer |
| sources | array | Retrieved source chunks |
| metrics | object | Retrieval and generation statistics |

---

## SourceChunk

| Field | Type | Description |
|--------|------|-------------|
| text | string | Retrieved chunk |
| score | float | Similarity score |
| file_name | string | Source document |
| page_label | string | Display page |
| page_number | integer | Original page number |
| chunk_index | integer | Chunk order within the document |
| chunk_length | integer | Length of the chunk |
| chunk_id | string | Internal chunk identifier |

---

## QueryMetrics

| Field | Type | Description |
|--------|------|-------------|
| retrieval_time_ms | float | Retrieval duration |
| generation_time_ms | float | LLM generation duration |
| total_time_ms | float | Total request latency |
| chunks_retrieved | integer | Number of retrieved chunks |
| average_similarity | float | Average similarity score |
| highest_similarity | float | Highest similarity score |

---

# Error Responses

## Invalid Request

```json
{
    "detail": "Query must contain at least three characters."
}
```

---

## Unsupported Document

```json
{
    "detail": "Unsupported document format."
}
```

---

## Empty Document

```json
{
    "detail": "No text could be extracted from the uploaded document."
}
```

---

## Collection Not Found

```json
{
    "detail": "Knowledge collection not found."
}
```

---

## Internal Server Error

```json
{
    "detail": "Internal server error."
}
```

---

# Performance

Typical execution times observed during development:

| Stage | Approximate Time |
|---------|-----------------:|
| Query Embedding | 5–20 ms |
| Dense Retrieval | 10–40 ms |
| BM25 Retrieval | 5–20 ms |
| Graph Retrieval | 10–50 ms |
| Cross Encoder Reranking | 50–200 ms |
| LLM Generation | 300–1500 ms |

Actual latency depends on document size, collection size, hardware, and language model response time.

---

# Authentication

The Knowledge Module is intended to operate behind the SynapseOS authentication and authorization layer.

Future enhancements include:

- JWT authentication
- Role-Based Access Control (RBAC)
- Multi-tenant document isolation
- API rate limiting
- Audit logging

---

# API Design Principles

The API follows several design principles:

- RESTful endpoints
- Stateless communication
- JSON request and response payloads
- Consistent response schemas
- Source attribution for explainability
- Modular integration with the SynapseOS platform

---

# Summary

The Knowledge Module API provides a simple yet extensible interface for enterprise document ingestion and question answering. By combining hybrid retrieval, graph retrieval, neural reranking, and grounded language generation, the API delivers explainable, context-aware responses suitable for enterprise knowledge applications.