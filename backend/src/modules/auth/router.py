from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.schemas import (
    RegisterRequest,
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
            "tenant_id": str(result["tenant"].id),
            "user_id": str(result["user"].id),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return JWT tokens.
    """

    try:

        service = AuthService(db)

        result = service.login(
            email=form_data.username,
            password=form_data.password,
        )

        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            user_id=str(result["user"].id),
            role=result["user"].role.value,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )