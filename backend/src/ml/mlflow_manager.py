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

            # Main algorithm
            mlflow.log_param(
                "algorithm",
                algorithm,
            )

            # Dataset information
            mlflow.log_params(
                metrics["dataset"],
            )

            # Training information
            mlflow.log_params(
                metrics["training"],
            )

            # Evaluation metrics (must be numeric)
            mlflow.log_metrics(
                metrics["metrics"],
            )

            # Save model artifact
            mlflow.log_artifact(
                artifact_path,
            )