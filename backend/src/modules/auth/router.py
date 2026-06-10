from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.core.security import (
    get_current_user,
)
from src.db.session import get_db
from src.modules.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    AccessTokenResponse,
    LogoutRequest
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
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):

    try:
        service = AuthService(db)

        result = service.login(
            payload.email,
            payload.password,
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


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role.value,
        "tenant_id": str(current_user.tenant_id),
    }


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    try:
        service = AuthService(db)

        access_token = service.refresh_access_token(payload.refresh_token)

        return AccessTokenResponse(access_token=access_token)

    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )


@router.post("/logout")
def logout(
    payload: LogoutRequest,
    db: Session = Depends(get_db),
):

    try:

        service = AuthService(db)

        service.logout(
            payload.refresh_token
        )

        return {
            "message": "Logged out successfully"
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )