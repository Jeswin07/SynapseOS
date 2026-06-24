"""Enterprise document loader."""

from __future__ import annotations

from pathlib import Path

import fitz
import pandas as pd
from docx import Document


class DocumentLoader:
    """
    Loads enterprise documents into plain text.

    Supported formats
    -----------------
    - PDF
    - TXT
    - MD
    - CSV
    - DOCX
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".md",
        ".csv",
        ".docx",
    }

    def load(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Returns

        [
            {
                "text": "...",
                "page_label": "1"
            }
        ]
        """

        path = Path(file_path)

        suffix = path.suffix.lower()

        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

        if suffix == ".pdf":
            return self._load_pdf(path)

        if suffix == ".csv":
            return self._load_csv(path)

        if suffix == ".docx":
            return self._load_docx(path)

        return self._load_text(path)

    # --------------------------------------------------

    def _load_pdf(
        self,
        path: Path,
    ) -> list[dict]:

        pages: list[dict] = []

        pdf = fitz.open(path)

        try:

            for index, page in enumerate(pdf):

                text = page.get_text(
                    "text"
                ).strip()

                if not text:
                    continue

                pages.append(
                    {
                        "text": text,
                        "page_label": str(index + 1),
                    }
                )

        finally:
            pdf.close()

        return pages

    # --------------------------------------------------

    def _load_csv(
        self,
        path: Path,
    ) -> list[dict]:

        df = pd.read_csv(path)

        text = df.to_markdown(
            index=False,
        )

        return [
            {
                "text": text,
                "page_label": "1",
            }
        ]

    # --------------------------------------------------

    def _load_docx(
        self,
        path: Path,
    ) -> list[dict]:

        doc = Document(str(path))

        paragraphs = []

        for paragraph in doc.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return [
            {
                "text": "\n".join(paragraphs),
                "page_label": "1",
            }
        ]

    # --------------------------------------------------

    def _load_text(
        self,
        path: Path,
    ) -> list[dict]:

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return [
            {
                "text": text,
                "page_label": "1",
            }
        ]