# Knowledge Module Evaluation

# Introduction

A Retrieval-Augmented Generation (RAG) system cannot be evaluated solely by observing generated answers. The quality of a RAG pipeline depends on both its retrieval performance and its answer generation capability.

The Knowledge Intelligence module includes a dedicated evaluation framework that measures retrieval effectiveness, generation quality, and overall system performance using benchmark datasets and objective evaluation metrics.

The evaluation framework enables repeatable benchmarking, comparison of retrieval strategies, and continuous improvement of the knowledge system.

---

# Evaluation Objectives

The evaluation framework is designed to answer the following questions:

* Are the correct documents being retrieved?
* Are relevant chunks ranked near the top?
* Does the language model answer using retrieved context?
* Are generated answers factually correct?
* Does the retrieval pipeline provide sufficient evidence?
* How quickly does the system respond?

---

# Evaluation Architecture

```text
                   Benchmark Dataset
                           │
                           ▼
                  Evaluation Framework
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
    Retrieval Evaluation          Generation Evaluation
            │                             │
            ▼                             ▼
     Retrieval Metrics           LLM Judge + Semantic Similarity
            │                             │
            └──────────────┬──────────────┘
                           ▼
                   Evaluation Report
```

---

# Benchmark Dataset

Evaluation is performed using manually curated benchmark datasets representing realistic enterprise information needs.

Each benchmark case contains:

* Question
* Expected Answer
* Expected Documents
* Expected Pages
* Difficulty
* Category

Example:

```json
{
    "id": "DATA_015",
    "difficulty": "hard",
    "category": "dataset",
    "question": "How would you identify repeat customers using the available datasets?",
    "expected_answer": "...",
    "expected_documents": [
        "olist_data_catalog.pdf"
    ],
    "expected_pages": [
        "7",
        "8",
        "13"
    ]
}
```

This structure enables both retrieval-level and generation-level evaluation using the same benchmark dataset.

---

# Retrieval Evaluation

Retrieval evaluation measures how effectively the system retrieves relevant context before answer generation.

## Precision@K

Precision@K measures the proportion of retrieved chunks that are relevant.

Formula:

```text
Relevant Retrieved Chunks
──────────────────────────
Total Retrieved Chunks
```

Higher values indicate that the retrieval pipeline returns fewer irrelevant chunks.

---

## Recall@K

Recall@K measures how much of the expected information was successfully retrieved.

Formula:

```text
Relevant Retrieved Chunks
──────────────────────────
Total Relevant Chunks
```

A higher Recall@K indicates that the retrieval stage successfully discovers most of the required evidence.

---

## Hit Rate

Hit Rate measures whether at least one relevant document appears within the retrieved Top-K results.

Formula:

```text
Queries with a Hit
──────────────────
Total Queries
```

This metric provides an intuitive indication of retrieval success.

---

## Mean Reciprocal Rank (MRR)

MRR measures how early the first relevant result appears.

Formula:

```text
1
────────────
Rank of First Relevant Result
```

Higher MRR values indicate better ranking quality.

---

## Average Similarity

Average cosine similarity between the user query and retrieved chunks.

This metric provides insight into semantic alignment between retrieved context and the original question.

---

## Highest Similarity

The maximum similarity score among retrieved chunks.

Useful for analyzing retrieval confidence.

---

## Retrieval Latency

Measures the average time required for:

* Query embedding
* Retrieval
* Hybrid fusion
* Graph retrieval
* Cross-encoder reranking

Latency is reported in milliseconds.

---

# Generation Evaluation

Retrieval alone does not guarantee correct answers.

Generation evaluation measures the quality of responses produced by the language model.

The Knowledge Intelligence module evaluates five complementary metrics.

---

## Faithfulness

Measures whether every factual statement in the generated answer is supported by the retrieved context.

Questions answered:

* Did the model hallucinate?
* Are unsupported facts introduced?

Higher scores indicate stronger grounding.

---

## Answer Correctness

Measures factual agreement between the generated answer and the benchmark reference answer.

This metric focuses on correctness rather than wording.

---

## Answer Relevancy

Measures whether the generated answer directly addresses the user's question.

Answers that are accurate but off-topic receive lower scores.

---

## Context Recall

Measures whether the retrieved context contained sufficient information to answer the question completely.

Low Context Recall generally indicates retrieval limitations rather than language model limitations.

---

## Semantic Similarity

Semantic Similarity is computed locally using Sentence Transformers.

Rather than comparing exact wording, it measures whether the generated answer and reference answer convey the same meaning.

Advantages:

* Robust to paraphrasing
* Independent of exact wording
* Fast local evaluation
* No external API calls

---

# LLM-as-a-Judge

The first four generation metrics are evaluated using a dedicated LLM Judge.

The evaluation prompt compares:

* User Question
* Retrieved Context
* Generated Answer
* Reference Answer

The judge returns structured scores for:

* Faithfulness
* Answer Correctness
* Answer Relevancy
* Context Recall

To improve efficiency, all four metrics are produced in a single LLM request.

---

# Why Not RAGAS?

RAGAS is a widely used evaluation framework for Retrieval-Augmented Generation systems.

During development, RAGAS was evaluated as a potential solution. However, dependency compatibility issues with the project's library versions and additional framework complexity made direct integration impractical within the project timeline.

Instead, the project implements a custom evaluation framework inspired by the same evaluation principles.

Advantages of the custom framework include:

* Full control over evaluation prompts
* Easy integration with the existing architecture
* Lower implementation complexity
* Production-oriented design
* Ability to customize metrics and reporting

The selected metrics align closely with commonly used RAG evaluation practices while remaining lightweight and maintainable.

---

# Evaluation Workflow

```text
Benchmark Question
        │
        ▼
Knowledge Retrieval
        │
        ▼
Answer Generation
        │
        ▼
LLM Judge
        │
        ├── Faithfulness
        ├── Correctness
        ├── Relevancy
        └── Context Recall
        │
        ▼
Sentence Transformer
        │
        ▼
Semantic Similarity
        │
        ▼
Evaluation Report
```

---

# Evaluation Reports

Each benchmark execution produces a structured report containing:

* Pipeline information
* Number of benchmark questions
* Retrieval metrics
* Generation metrics
* Latency measurements
* Per-question evaluation results

Reports are stored as JSON files to support future comparison and regression testing.

---

# Current Evaluation Coverage

The current evaluation framework supports:

### Retrieval

* Precision@K
* Recall@K
* Hit Rate
* Mean Reciprocal Rank (MRR)
* Average Similarity
* Highest Similarity
* Retrieval Latency

### Generation

* Faithfulness
* Answer Correctness
* Answer Relevancy
* Context Recall
* Semantic Similarity

---

# Current Limitations

The evaluation framework currently has the following limitations:

* Benchmark datasets are manually curated.
* Human evaluation is not included.
* Generation evaluation depends partly on an LLM judge.
* Domain coverage is limited to the available enterprise documents.
* Long-form conversational evaluation is outside the current scope.

These limitations provide opportunities for future enhancement.

---

# Future Enhancements

Potential improvements include:

* Integration with RAGAS when ecosystem compatibility improves.
* Automated benchmark generation.
* Human evaluation workflows.
* Multi-turn conversation evaluation.
* Domain-specific benchmark suites.
* Continuous evaluation in CI/CD pipelines.
* Dashboard-based evaluation visualization.

---

# Summary

The Knowledge Intelligence module includes a comprehensive evaluation framework covering both retrieval and answer generation.

Rather than relying on subjective inspection, the system uses benchmark datasets and quantitative metrics to measure retrieval effectiveness, answer quality, contextual grounding, and overall performance.

This evaluation-first approach enables systematic comparison of retrieval strategies, supports continuous improvement, and provides confidence that generated answers remain accurate, relevant, and grounded in enterprise knowledge.
