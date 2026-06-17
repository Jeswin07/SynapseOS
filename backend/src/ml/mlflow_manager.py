import mlflow


class MLflowManager:
    """
    Handles MLflow experiment tracking.
    """

    def __init__(self) -> None:

        mlflow.set_tracking_uri(
            "sqlite:///mlflow.db",
        )

        mlflow.set_experiment(
            "SynapseOS",
        )

    def log_training(
        self,
        *,
        algorithm: str,
        metrics: dict,
        artifact_path: str,
    ) -> None:

        with mlflow.start_run():

            mlflow.log_param(
                "algorithm",
                algorithm,
            )

            mlflow.log_metrics(
                metrics,
            )

            mlflow.log_artifact(
                artifact_path,
            )