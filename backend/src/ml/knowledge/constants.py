"""Constants used by the Knowledge Intelligence module."""

from __future__ import annotations

# ==========================================================
# Payload Keys (Qdrant)
# ==========================================================

TEXT = "text"

DOCUMENT_ID = "document_id"

FILE_NAME = "file_name"

FILE_TYPE = "file_type"

PAGE_LABEL = "page_label"

CHUNK_ID = "chunk_id"

CHUNK_INDEX = "chunk_index"

CHUNK_LENGTH = "chunk_length"

UPLOADED_AT = "uploaded_at"


# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_DOCUMENT_TYPES = (
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".csv",
)


# ==========================================================
# Misc
# ==========================================================

UNKNOWN = "Unknown"

DEFAULT_PAGE = "1"