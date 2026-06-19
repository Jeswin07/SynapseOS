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
from src.modules.risk.schemas import (
    RiskRequest,
    RiskResponse,
)
from src.modules.risk.service import (
    RiskService,
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk"],
)


@router.post(
    "/analyze",
    response_model=RiskResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_risk(
    payload: RiskRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Analyze dataset risk.
    """

    try:

        service = RiskService(db)

        risk, result = service.analyze(
            dataset_id=payload.dataset_id,
            created_by=current_user.id,
        )

        return RiskResponse(
            analysis_id=risk.id,
            risk_score=risk.risk_score,
            risk_level=risk.risk_level,
            anomalies=risk.anomalies,
            rows=result["rows"],
            message="Risk analysis completed successfully.",
            summary=result["summary"]
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )