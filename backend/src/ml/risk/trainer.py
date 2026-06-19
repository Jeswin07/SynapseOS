from src.ml.preprocessing.loader import (
    DatasetLoader,
)
from src.ml.risk.detector import (
    RiskDetector,
)


class RiskTrainer:

    def __init__(self):

        self.loader = DatasetLoader()

        self.detector = RiskDetector()

    def analyze(
        self,
        *,
        storage_path: str,
    ):

        dataframe = self.loader.load_csv(
            storage_path,
        )

        return self.detector.analyze(
            dataframe,
        )