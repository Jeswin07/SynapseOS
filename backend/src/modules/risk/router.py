"""Risk API router."""

from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from src.db.session import get_db

from src.modules.auth.dependencies import (
    get_current_user,
)

from src.modules.risk.schemas import (
    RiskResponse,
)

from src.modules.risk.service import (
    RiskService,
)


router = APIRouter(
    prefix="/risks",
    tags=[
        "Risks",
    ],
)


@router.get(
    "/analyze",
    response_model=RiskResponse,
)
def analyze_risk(
    db: Session = Depends(
        get_db,
    ),
    user=Depends(
        get_current_user,
    ),
):
    """
    Analyze business risks.
    """

    service = RiskService(
        db,
    )


    return service.analyze(
        created_by=user.id,
    )