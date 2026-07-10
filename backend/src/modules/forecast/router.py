from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.dependencies import (
    get_current_user,
)
from src.modules.forecast.schemas import (
    ForecastPoint,
    ForecastPredictRequest,
    ForecastPredictResponse,
    TrainForecastRequest,
    TrainForecastResponse,
)
from src.modules.forecast.service import (
    ForecastService,
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


@router.post(
    "/train",
    response_model=TrainForecastResponse,
    status_code=status.HTTP_201_CREATED,
)
async def train_forecast(
    payload: TrainForecastRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Train a Prophet forecasting model.
    """

    try:

        service = ForecastService(db)

        forecast = await service.train(
        dataset_version_id=payload.dataset_version_id,
        created_by=current_user.id,
        query=(
            payload.query or "forecast revenue"
        ),
    )

        return TrainForecastResponse(
            forecast_id=forecast.id,
            message="Forecast model trained successfully.",
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
    
@router.post(
    "/predict",
    response_model=ForecastPredictResponse,
)
def predict_forecast(
    payload: ForecastPredictRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = ForecastService(db)

    forecast = service.predict(
        forecast_id=payload.forecast_id,
        periods=payload.periods,
    )

    return ForecastPredictResponse(
        forecast=[
            ForecastPoint(**point)
            for point in forecast
        ]
    )