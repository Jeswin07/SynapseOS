import polars as pl
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class DataPreprocessor:
    """
    Preprocess datasets for machine learning.
    """

    def prepare(
        self,
        df: pl.DataFrame,
        *,
        target_column: str,
        time_column: str | None = None,
    ):
        """
        Prepare features and target for training.

        Args:
            df: Input dataframe.
            target_column: Target variable.
            time_column: Optional datetime column.

        Returns:
            Tuple of:
                - transformed features
                - target
                - fitted preprocessor
        """

        feature_df = df

        if time_column and time_column in feature_df.columns:
            feature_df = feature_df.drop(time_column)

        feature_df = feature_df.drop(target_column)

        #
        # Remove obvious identifier columns
        #
        id_columns = [
            column
            for column in feature_df.columns
            if column.lower().endswith("id")
            or column.lower().endswith("_id")
        ]

        if id_columns:
            feature_df = feature_df.drop(id_columns)

        #
        # Convert to pandas for sklearn
        #
        x = feature_df.to_pandas()

        y = df[target_column].to_pandas()

        categorical_columns = (
            x.select_dtypes(
                include=["object", "category"],
            )
            .columns
            .tolist()
        )

        numeric_columns = (
            x.select_dtypes(
                exclude=["object", "category"],
            )
            .columns
            .tolist()
        )

        numeric_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent",
                    ),
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore",
                    ),
                ),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "numeric",
                    numeric_pipeline,
                    numeric_columns,
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    categorical_columns,
                ),
            ]
        )

        x_processed = preprocessor.fit_transform(x)

        return (
            x_processed,
            y,
            preprocessor,
        )