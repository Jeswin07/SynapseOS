"""Detect logical dataset file names."""

from __future__ import annotations


class LogicalNameDetector:
    """
    Detect business meaning of uploaded files.
    """

    RULES = [
        (
            "order_items",
            [
                "order_items",
                "order_item",
            ],
        ),
        (
            "payments",
            [
                "payment",
                "payments",
                "billing",
                "invoice",
            ],
        ),
        (
            "reviews",
            [
                "review",
                "reviews",
                "rating",
                "feedback",
            ],
        ),
        (
            "category_translation",
            [
                "category_translation",
                "translation",
            ],
        ),
        (
            "customers",
            [
                "customer",
                "customers",
                "client",
            ],
        ),
        (
            "products",
            [
                "products",
                "product",
                "catalog",
            ],
        ),
        (
            "sellers",
            [
                "seller",
                "sellers",
                "vendor",
                "merchant",
            ],
        ),
        (
            "geolocation",
            [
                "geo",
                "location",
                "address",
            ],
        ),
        (
            "orders",
            [
                "orders",
                "transaction",
                "sales",
            ],
        ),
    ]


    @classmethod
    def detect(
        cls,
        filename: str,
    ) -> str:

        normalized = (
            filename.lower()
            .replace(".csv", "")
            .replace(".xlsx", "")
            .replace("-", "_")
        )

        for logical_name, keywords in cls.RULES:

            for keyword in keywords:

                if keyword in normalized:
                    return logical_name

        return normalized