from abc import ABC, abstractmethod
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer


@dataclass(slots=True)
class TrainingResult:
    """
    Result returned after model training.
    """

    model: object

    preprocessor: ColumnTransformer

    x_test: object

    y_test: object


class BaseAlgorithm(ABC):
    """
    Base class for all ML algorithms.
    """

    name: str

    @abstractmethod
    def train(
        self,
        dataframe,
        target_column: str,
        time_column: str,
    ) -> TrainingResult:
        """
        Train a model.
        """

    @abstractmethod
    def save(
        self,
        model,
        preprocessor,
        path: str,
    ) -> None:
        """
        Save trained model.
        """

    @abstractmethod
    def predict(
        self,
        model,
        preprocessor,
        dataframe,
    ):
        ...

class PredictionResult:

    def __init__(
        self,
        predictions,
    ):

        self.predictions = predictions