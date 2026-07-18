"""Generic dataset filtering schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class DatasetFilters(BaseModel):
    """
    Generic dataset filters.

    These filters operate on the canonical feature names
    produced by the Feature Builder.

    They are intentionally dataset-agnostic, allowing the
    same filtering logic to work across Olist, Flipkart,
    and any future commerce dataset.
    """

    # ------------------------------------------------------------------
    # Date Filters
    # ------------------------------------------------------------------

    date_from: str | None = None
    date_to: str | None = None

    # ------------------------------------------------------------------
    # Geography
    # ------------------------------------------------------------------

    states: list[str] = Field(default_factory=list)
    city: list[str] = Field(default_factory=list)

    # ------------------------------------------------------------------
    # Commerce
    # ------------------------------------------------------------------

    categories: list[str] = Field(default_factory=list)
    brands: list[str] = Field(default_factory=list)

    seller_id: list[str] = Field(default_factory=list)
    customer_id: list[str] = Field(default_factory=list)

    # ------------------------------------------------------------------
    # Revenue
    # ------------------------------------------------------------------

    min_revenue: float | None = None
    max_revenue: float | None = None

    # ------------------------------------------------------------------
    # Reviews
    # ------------------------------------------------------------------

    min_review_score: float | None = None
    max_review_score: float | None = None