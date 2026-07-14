"""Prediction API routes."""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.dependencies import (
    get_current_user,
)
from src.modules.prediction.schemas import (
    PredictionRequest,
)
from src.modules.prediction.service import (
    PredictionService,
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/run",
)
async def run_prediction(
    payload: PredictionRequest,
    current_user=Depends(
        get_current_user,
    ),
    db: Session = Depends(
        get_db,
    ),
):
    """
    Run ML prediction.
    """

    try:

        service = PredictionService(
            db,
        )

        result = service.predict(
            dataset_version_id=payload.dataset_version_id,
            prediction_type=payload.prediction_type,
            created_by=current_user.id,
        )

        return result


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.get(
    "/history",
)
async def prediction_history(
    current_user=Depends(
        get_current_user,
    ),
    db: Session = Depends(
        get_db,
    ),
):
    """
    Get prediction execution history.
    """

    service = PredictionService(
        db,
    )

    return service.history(
        created_by=current_user.id,
    )