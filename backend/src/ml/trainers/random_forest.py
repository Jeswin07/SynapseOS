import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from src.ml.algorithms.base import (
    BaseAlgorithm,
    TrainingResult,
)
from src.ml.preprocessing.preprocessor import (
    DataPreprocessor,
)


class RandomForestTrainer(BaseAlgorithm):
    """
    Random Forest regression trainer.
    """

    name = "random_forest"

    def train(
        self,
        dataframe,
        target_column: str,
        time_column: str,
    ) -> TrainingResult:
        """
        Train a Random Forest regression model.
        """

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

        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1,
        )

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
        """
        Save trained model and preprocessing pipeline.
        """

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
        """
        Generate predictions.
        """

        transformed = preprocessor.transform(
            dataframe.to_pandas(),
        )

        predictions = model.predict(
            transformed,
        )

        return predictions.tolist()