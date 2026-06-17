from pathlib import Path

import polars as pl


class DatasetExporter:
    """
    Export processed dataset.
    """

    def export(
        self,
        dataframe: pl.DataFrame,
        output_path: str | Path,
    ) -> None:
        """
        Export dataframe to CSV.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.write_csv(
            output_path,
        )

        print(
            f"\nDataset exported to:\n{output_path}"
        )

        print(
            f"Rows    : {dataframe.height}"
        )

        print(
            f"Columns : {dataframe.width}"
        )