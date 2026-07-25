from pathlib import Path

ARTIFACTS_DIR = Path("/app/artifacts")

FORECAST_ARTIFACTS_DIR = ARTIFACTS_DIR / "forecast"
MODEL_ARTIFACTS_DIR = ARTIFACTS_DIR / "models"
EVALUATION_ARTIFACTS_DIR = ARTIFACTS_DIR / "evaluation"


def ensure_artifact_directories() -> None:
    """
    Create all artifact directories if they do not exist.
    """
    FORECAST_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    EVALUATION_ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)