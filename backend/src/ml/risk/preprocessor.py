import polars as pl
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class RiskPreprocessor:
    """
    Preprocessing pipeline for anomaly detection.
    """

    MAX_CARDINALITY = 100

    def prepare(
        self,
        dataframe: pl.DataFrame,
    ):
        """
        Prepare data for Isolation Forest.
        """

        dataframe = dataframe.drop_nulls()

        #
        # Remove ID columns
        #
        id_columns = [
            column
            for column in dataframe.columns
            if (
                column.lower().endswith("id")
                or column.lower().endswith("_id")
                or "unique" in column.lower()
            )
        ]

        if id_columns:
            dataframe = dataframe.drop(id_columns)

        #
        # Remove datetime columns
        #
        datetime_columns = [
            column
            for column, dtype in zip(
                dataframe.columns,
                dataframe.dtypes,
            )
            if dtype == pl.Datetime
        ]

        if datetime_columns:
            dataframe = dataframe.drop(
                datetime_columns,
            )

        pandas_df = dataframe.to_pandas()

        #
        # Detect categorical columns
        #
        categorical_columns = []

        numeric_columns = []

        for column in pandas_df.columns:

            if pandas_df[column].dtype == "object":

                #
                # Ignore high-cardinality columns
                #
                if (
                    pandas_df[column]
                    .nunique()
                    <= self.MAX_CARDINALITY
                ):
                    categorical_columns.append(
                        column,
                    )

            else:

                numeric_columns.append(
                    column,
                )

        numeric_pipeline = Pipeline(
            [
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median",
                    ),
                ),
            ]
        )

        categorical_pipeline = Pipeline(
            [
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

        transformer = ColumnTransformer(
            [
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

        x = transformer.fit_transform(
            pandas_df,
        )

        return (
            x,
            transformer,
        )