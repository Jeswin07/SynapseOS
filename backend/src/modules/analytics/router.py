"""Analytics routes."""

from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.analytics.schemas import (
    AnalyticsRequest,
)
from src.modules.analytics.service import (
    AnalyticsService,
)
from src.modules.auth.dependencies import (
    get_current_user,
)

router = APIRouter(
    prefix="/analytics",
    tags=[
        "Analytics",
    ],
)


@router.post(
    "/run",
)
def run_analytics(
    request: AnalyticsRequest,
    current_user=Depends(
        get_current_user,
    ),
    db: Session = Depends(
        get_db,
    ),
):

    service = AnalyticsService(
        db,
    )


    return service.analyze(
        request.dataset_version_id,
    )