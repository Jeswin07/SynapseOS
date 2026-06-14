from io import BytesIO

import polars as pl


class DatasetProfiler:
    """
    Generate basic statistics for uploaded datasets.
    """

    def profile(
        self,
        file_bytes: bytes,
    ) -> dict:
        """
        Profile a CSV dataset.

        Args:
            file_bytes: Uploaded file content.

        Returns:
            Dataset statistics.
        """

        df = pl.read_csv(
            BytesIO(file_bytes),
        )

        return {
            "row_count": df.height,
            "column_count": df.width,
            "columns": df.columns,
            "dtypes": {
                column: str(dtype)
                for column, dtype in zip(
                    df.columns,
                    df.dtypes,
                )
            },
            "null_count": (
                df.null_count()
                .to_dicts()[0]
            ),
            "duplicate_rows": (
                df.height
                - df.unique().height
            ),
        }