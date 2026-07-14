# Cross-Encoder Reranking

# Introduction

Retrieval systems often prioritize recall by retrieving a broad set of potentially relevant document chunks. While this increases the likelihood of finding useful information, it also introduces less relevant results into the candidate set.

To improve ranking quality, the Knowledge Intelligence module applies a Cross-Encoder reranking stage after hybrid and graph retrieval.

Unlike embedding-based retrieval, which compares vectors independently, a Cross Encoder jointly evaluates the user query and each candidate chunk, producing significantly more accurate relevance scores.

---

# Objectives

The reranking stage is designed to:

* Improve ranking accuracy
* Remove noisy retrieval results
* Prioritize highly relevant context
* Improve answer quality
* Reduce hallucination
* Increase retrieval precision

---

# Why Reranking?

Dense retrieval is optimized for speed.

BM25 is optimized for exact keyword matching.

Graph retrieval is optimized for contextual expansion.

Each retrieval strategy contributes useful information, but none is perfect.

A Cross Encoder performs a final, more precise evaluation of every retrieved candidate before it is sent to the language model.

---

# Retrieval Before Reranking

After hybrid retrieval and graph expansion, the system may have a candidate pool like this:

| Rank | Chunk   | Retrieval Source |
| ---- | ------- | ---------------- |
| 1    | Chunk A | Dense Retrieval  |
| 2    | Chunk B | BM25             |
| 3    | Chunk C | Graph Retrieval  |
| 4    | Chunk D | Dense Retrieval  |
| 5    | Chunk E | BM25             |
| 6    | Chunk F | Graph Retrieval  |

Some chunks are only loosely related to the user's question.

The reranker determines which chunks are actually most relevant.

---

# How a Cross Encoder Works

Unlike bi-encoder retrieval, a Cross Encoder evaluates the query and document together.

Instead of comparing two independent embedding vectors, it processes:

```text
(Query, Candidate Chunk)
```

as a single input.

Example:

```text
Query:
How are customer payments related to orders?

Candidate Chunk:
Payments are associated with orders using the order_id field.
```

The model directly predicts how relevant the chunk is to the query.

---

# Bi-Encoder vs Cross Encoder

| Bi-Encoder                            | Cross Encoder                       |
| ------------------------------------- | ----------------------------------- |
| Encodes query and document separately | Encodes query and document together |
| Extremely fast                        | Slower                              |
| Suitable for large-scale retrieval    | Suitable for reranking              |
| Uses cosine similarity                | Learns deep semantic interactions   |
| Lower ranking quality                 | Higher ranking quality              |

The system combines both approaches:

* Bi-Encoder for efficient retrieval
* Cross Encoder for accurate ranking

---

# Position in the Pipeline

```text
User Query
      │
      ▼
Hybrid Retrieval
(Dense + BM25)
      │
      ▼
Graph Retrieval
      │
      ▼
Candidate Pool
      │
      ▼
Cross Encoder
      │
      ▼
Top-K Context
      │
      ▼
Groq LLM
```

The Cross Encoder acts as the final retrieval stage before answer generation.

---

# Candidate Evaluation

Each retrieved chunk is independently scored.

```text
(Query, Chunk A) → 0.97

(Query, Chunk B) → 0.82

(Query, Chunk C) → 0.91

(Query, Chunk D) → 0.43
```

Chunks are then sorted according to these scores.

Only the highest-ranked chunks are forwarded to the language model.

---

# Why Not Use the Cross Encoder First?

A Cross Encoder is computationally expensive because it evaluates one query-document pair at a time.

Evaluating thousands of chunks would be impractical.

Instead, the system follows a two-stage retrieval strategy:

1. Fast retrieval generates a candidate set.
2. The Cross Encoder reranks only those candidates.

This balances retrieval quality with response latency.

---

# Benefits

The reranking stage provides several advantages:

### Improved Precision

Less relevant chunks are removed before answer generation.

---

### Better Context Quality

The language model receives higher-quality evidence.

---

### Reduced Hallucination

Accurate context reduces the likelihood of unsupported responses.

---

### Better Semantic Understanding

The Cross Encoder captures interactions between the query and document that cosine similarity cannot.

---

### Improved Answer Quality

Higher-quality retrieval generally produces more accurate and complete answers.

---

# Trade-Offs

The primary trade-off is additional latency.

| Without Reranking      | With Reranking            |
| ---------------------- | ------------------------- |
| Faster retrieval       | Slightly slower retrieval |
| Lower ranking accuracy | Higher ranking accuracy   |
| More noisy context     | Cleaner context           |
| Lower answer quality   | Better grounded answers   |

The increase in latency is typically acceptable because reranking is applied only to a small candidate set.

---

# Current Implementation

The Knowledge Intelligence module applies the Cross Encoder after:

* Dense Retrieval
* BM25 Retrieval
* Reciprocal Rank Fusion
* Graph Retrieval

The reranker receives the combined candidate pool, assigns a relevance score to each chunk, and returns the highest-ranked results for answer generation.

---

# Future Enhancements

Potential improvements include:

* Adaptive reranking thresholds
* Dynamic Top-K selection
* Learning-to-rank models
* Domain-specific Cross Encoders
* GPU-accelerated inference
* Batch reranking optimization

---

# Summary

The Cross Encoder serves as the final retrieval refinement stage.

Rather than replacing hybrid retrieval, it enhances it by improving the ordering of candidate chunks before they reach the language model.

This two-stage retrieval strategy combines the efficiency of embedding-based retrieval with the accuracy of deep neural ranking, resulting in more precise, contextually grounded, and reliable enterprise question answering.
