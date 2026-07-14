# Configuration

# Introduction

The Knowledge Intelligence module is highly configurable through environment variables and application settings. Centralizing configuration enables deployment across development, staging, and production environments without modifying the application code.

Configuration controls document ingestion, retrieval behavior, embedding generation, graph connectivity, language model selection, and evaluation settings.

---

# Configuration Overview

The Knowledge module relies on several external services.

```text
                Configuration
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
   Qdrant         Neo4j            Groq API
      │               │                │
      └───────────────┼────────────────┘
                      ▼
              Knowledge Module
```

---

# Environment Variables

## Qdrant

| Variable | Description |
|----------|-------------|
| QDRANT_URL | URL of the Qdrant server |
| KNOWLEDGE_COLLECTION | Default vector collection |

Example

```env
QDRANT_URL=http://localhost:6333
KNOWLEDGE_COLLECTION=enterprise_docs_v5
```

---

## Neo4j

| Variable | Description |
|----------|-------------|
| NEO4J_URI | Neo4j database URI |
| NEO4J_USERNAME | Database username |
| NEO4J_PASSWORD | Database password |

Example

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

---

## Groq

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | Groq API Key |
| GROQ_MODEL | Model used for answer generation |
| GROQ_JUDGE_MODEL | Model used for LLM evaluation |

Example

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_JUDGE_MODEL=llama-3.1-8b-instant
```

---

## Embedding Model

| Variable | Description |
|----------|-------------|
| EMBEDDING_MODEL | Sentence Transformer model |

Example

```env
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

---

## Cross Encoder

| Variable | Description |
|----------|-------------|
| RERANKER_MODEL | Cross Encoder model |

Example

```env
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
```

---

## Retrieval

| Variable | Description |
|----------|-------------|
| TOP_K | Number of chunks returned |
| HYBRID_ALPHA | Hybrid retrieval weighting (future enhancement) |

Example

```env
TOP_K=5
```

---

# Application Configuration

The configuration is loaded through the application's `Settings` class.

Typical configuration categories include:

- Vector database
- Graph database
- Embedding models
- Language models
- Retrieval parameters
- Evaluation settings

Centralizing configuration simplifies deployment and maintenance.

---

# Recommended Development Configuration

| Component | Recommendation |
|-----------|----------------|
| Qdrant | Local Docker |
| Neo4j | Local Docker |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Cross Encoder | ms-marco-MiniLM-L-6-v2 |
| LLM | Groq |
| Collection | enterprise_docs_v5 |

---

# Production Considerations

For production deployments, consider:

- Secure storage of API keys
- Environment-specific configuration
- Secrets management
- HTTPS endpoints
- Database authentication
- Monitoring and logging

Configuration values should never be hardcoded within the application.

---

# Summary

The Knowledge Intelligence module centralizes configuration to support flexible deployment across different environments while keeping retrieval, generation, and evaluation settings consistent and maintainable.