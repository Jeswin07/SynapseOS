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

        user = service.register(
            email=payload.email,
            full_name=payload.full_name,
            password=payload.password,
            tenant_id=payload.tenant_id,
        )

        return {
            "message": "User created",
            "user_id": str(user.id),
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
    payload: LoginRequest,
    db: Session = Depends(get_db),
):

    try:

        service = AuthService(db)

        token = service.login(
            payload.email,
            payload.password,
        )

        return TokenResponse(
            access_token=token,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )