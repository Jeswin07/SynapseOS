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

        print("=" * 60)
        print("Random Forest Training Started")
        print("=" * 60)

        print(f"Original dataset shape: {dataframe.shape}")

        preprocessor = DataPreprocessor()

        print("Preprocessing dataset...")

        x, y, preprocessing_pipeline = (
            preprocessor.prepare(
                dataframe,
                target_column=target_column,
                time_column=time_column,
            )
        )

        print("Preprocessing complete.")
        print(f"Processed feature matrix shape: {x.shape}")
        print(f"Target shape: {y.shape}")

        print("Splitting dataset...")

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=42,
        )

        print("Train/Test split complete.")
        print(f"x_train: {x_train.shape}")
        print(f"x_test : {x_test.shape}")

        print("Initializing Random Forest...")

        model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            verbose=2,
        )

        print("Starting model.fit()...")

        model.fit(
            x_train,
            y_train,
        )

        print("Model training complete.")

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

        print(f"Saving model to {path}")

        joblib.dump(
            {
                "model": model,
                "preprocessor": preprocessor,
            },
            path,
        )

        print("Model saved.")

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