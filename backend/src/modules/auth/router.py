from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.db.session import get_db

from src.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from src.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):

    try:

        service = AuthService(db)

        result = service.register(
            company_name=payload.company_name,
            industry=payload.industry,
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
        )

        return {
            "message": "Organization created successfully",
            "tenant_id": str(
                result["tenant"].id
            ),
            "user_id": str(
                result["user"].id
            ),
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )