"""Entity extraction for the Knowledge Graph."""

from __future__ import annotations

import re

import spacy
from spacy.matcher import PhraseMatcher

from src.ml.knowledge.graph.entity_dictionary import (
    BUSINESS_ENTITIES,
)


class EntityExtractor:
    """
    Extracts domain-specific business entities
    from document chunks.
    """

    def __init__(self) -> None:

        try:
            self.nlp = spacy.load(
                "en_core_web_sm",
                disable=[
                    "parser",
                    "textcat",
                ],
            )
        except OSError as e:
            raise RuntimeError(
                "SpaCy model 'en_core_web_sm' is missing."
            ) from e

        self.matcher = PhraseMatcher(
            self.nlp.vocab,
            attr="LOWER",
        )

        patterns = [
            self.nlp.make_doc(entity)
            for entity in BUSINESS_ENTITIES
        ]

        self.matcher.add(
            "BUSINESS_ENTITY",
            patterns,
        )

    @staticmethod
    def normalize(
        text: str,
    ) -> str:
        """
        Normalize extracted entities.
        """

        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    def extract(
        self,
        text: str,
    ) -> list[str]:
        """
        Extract business entities from text.
        """

        doc = self.nlp(text)

        entities: set[str] = set()

        # -----------------------
        # Phrase Matcher
        # -----------------------

        for _, start, end in self.matcher(doc):

            entity = self.normalize(
                doc[start:end].text
            )

            entities.add(entity)

        # -----------------------
        # Named Entities
        # -----------------------

        for ent in doc.ents:

            if ent.label_ in {
                "ORG",
                "PRODUCT",
                "LAW",
                "GPE",
            }:

                entities.add(
                    self.normalize(ent.text)
                )

        entities.update(
            self.extract_dataset_names(text)
        )

        return sorted(entities)
    
    @staticmethod
    def extract_dataset_names(
        text: str,
    ) -> set[str]:
        """
        Automatically extracts Olist dataset names.

        Examples
        --------
        olist_orders_dataset.csv
        olist_orders_dataset
        """

        pattern = r"olist_[a-zA-Z0-9_]+"

        matches = re.findall(
            pattern,
            text.lower(),
        )

        datasets = set()

        for match in matches:

            dataset = match.replace(
                ".csv",
                "",
            )

            datasets.add(dataset)

        return datasets