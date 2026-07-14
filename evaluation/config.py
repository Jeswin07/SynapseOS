"""Configuration for offline RAGAS evaluation."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "KNOWLEDGE_API",
    "http://127.0.0.1:8000/knowledge/query",
)

BENCHMARK_DIR = "../backend/datasets/knowledge/benchmark/v1"

OUTPUT_DIR = "reports"

TOP_K = 5