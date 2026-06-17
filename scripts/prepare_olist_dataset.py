from pathlib import Path

from etl.cleaning import DataCleaner
from etl.exporter import DatasetExporter
from etl.features import FeatureEngineer
from etl.joins import OlistJoiner
from etl.loaders import OlistLoader


def main() -> None:
    """
    Build the official SynapseOS ML dataset.
    """

    project_root = Path(__file__).resolve().parent.parent

    raw_path = (
        project_root
        / "datasets"
        / "raw"
        / "olist"
    )

    output_path = (
        project_root
        / "datasets"
        / "processed"
        / "olist_ml_dataset.csv"
    )

    print("=" * 60)
    print("Preparing Olist ML Dataset")
    print("=" * 60)

    datasets = OlistLoader(
        raw_path,
    ).load()

    dataframe = OlistJoiner().join(
        **datasets,
    )

    print(
        f"\nAfter joins : {dataframe.shape}"
    )

    dataframe = FeatureEngineer().transform(
        dataframe,
    )

    print(
        f"After feature engineering : {dataframe.shape}"
    )

    dataframe = DataCleaner().clean(
        dataframe,
    )

    print(
        f"After cleaning : {dataframe.shape}"
    )

    DatasetExporter().export(
        dataframe,
        output_path,
    )

    print("\nDone!")


if __name__ == "__main__":
    main()