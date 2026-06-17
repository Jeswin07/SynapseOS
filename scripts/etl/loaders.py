from pathlib import Path

import polars as pl


class OlistLoader:
    """
    Loads all required Olist datasets.
    """

    def __init__(
        self,
        raw_path: str | Path,
    ) -> None:

        self.raw_path = Path(raw_path)

    def load(self) -> dict[str, pl.DataFrame]:
        """
        Load all Olist CSV files.

        Returns:
            Dictionary of Polars DataFrames.
        """

        return {
            "orders": self._read(
                "olist_orders_dataset.csv",
            ),
            "order_items": self._read(
                "olist_order_items_dataset.csv",
            ),
            "products": self._read(
                "olist_products_dataset.csv",
            ),
            "customers": self._read(
                "olist_customers_dataset.csv",
            ),
            "payments": self._read(
                "olist_order_payments_dataset.csv",
            ),
            "reviews": self._read(
                "olist_order_reviews_dataset.csv",
            ),
            "translations": self._read(
                "product_category_name_translation.csv",
            ),
        }

    def _read(
        self,
        filename: str,
    ) -> pl.DataFrame:
        """
        Read a CSV file.
        """

        path = self.raw_path / filename

        print(f"Loading {filename}")

        return pl.read_csv(
            path,
            infer_schema_length=10000,
            try_parse_dates=True,
        )