import joblib
import polars as pl
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from src.ml.algorithms.base import (
    BaseAlgorithm,
    TrainingResult,
)
from src.ml.preprocessing.preprocessor import (
    DataPreprocessor,
)


class LinearRegressionTrainer(BaseAlgorithm):
    """
    Linear Regression algorithm implementation.
    """

    name = "linear_regression"

    def train(
        self,
        dataframe: pl.DataFrame,
        target_column: str,
        time_column: str,
    ) -> TrainingResult:

        preprocessor = DataPreprocessor()

        x, y, preprocessing_pipeline = (
            preprocessor.prepare(
                dataframe,
                target_column=target_column,
                time_column=time_column,
            )
        )

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=42,
        )

        model = LinearRegression()

        model.fit(
            x_train,
            y_train,
        )

        return TrainingResult(
            model=model,
            preprocessor=preprocessing_pipeline,
            x_test=x_test,
            y_test=y_test,
        )


    def save(
        self,
        model,
        preprocessor,
        path: str,
    ) -> None:

        joblib.dump(
            {
                "model": model,
                "preprocessor": preprocessor,
            },
            path,
        )

    def predict(
        self,
        model,
        preprocessor,
        dataframe,
    ):

        transformed = preprocessor.transform(
            dataframe.to_pandas(),
        )

        predictions = model.predict(
            transformed,
        )

        return predictions.tolist()