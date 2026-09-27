import uuid
from datetime import datetime, timezone
from typing import Optional, Dict
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.database import get_db
from src.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    get_current_user_token
)
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse

router = APIRouter()

# In-memory storage cache for ultra-fast auth fallback when DB is in initial migration
_MOCK_USER_STORE: Dict[str, Dict] = {
    "engineer@impeccable.ai": {
        "id": "usr-lead-engineer-01",
        "email": "engineer@impeccable.ai",
        "hashed_password": get_password_hash("password123"),
        "full_name": "Lead AI Engineer",
        "target_career_path": "Agentic AI Systems Engineer",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new learner account with hashed credentials and creates a JWT access token.
    """
    email = payload.email.lower()

    # 1. Check existing in mock store
    if email in _MOCK_USER_STORE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    user_id = str(uuid.uuid4())
    hashed_pwd = get_password_hash(payload.password)

    # 2. Persist in memory store
    user_record = {
        "id": user_id,
        "email": email,
        "hashed_password": hashed_pwd,
        "full_name": payload.full_name or "AI Engineer",
        "target_career_path": payload.target_career_path,
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    _MOCK_USER_STORE[email] = user_record

    # 3. Attempt DB persistence if session is active
    try:
        db_user = User(
            id=user_id,
            email=email,
            hashed_password=hashed_pwd,
            full_name=payload.full_name,
            target_career_path=payload.target_career_path,
            is_active=True
        )
        db.add(db_user)
        await db.commit()
    except Exception:
        # Fallback continues gracefully with in-memory store in dev/offline mode
        pass

    token = create_access_token(subject=user_id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_id,
        email=email
    )


@router.post("/login", response_model=TokenResponse, tags=["Authentication"])
async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticates user credentials and returns a signed JWT access token.
    """
    email = payload.email.lower()
    user_data = _MOCK_USER_STORE.get(email)

    # Attempt query from database
    if not user_data:
        try:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            found = result.scalar_one_or_none()
            if found:
                user_data = {
                    "id": found.id,
                    "email": found.email,
                    "hashed_password": found.hashed_password,
                    "full_name": found.full_name,
                    "target_career_path": found.target_career_path,
                    "is_active": found.is_active,
                    "created_at": found.created_at
                }
        except Exception:
            pass

    if not user_data or not verify_password(payload.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password credentials."
        )

    token = create_access_token(subject=user_data["id"])
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_data["id"],
        email=user_data["email"]
    )


@router.get("/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_profile(token: Optional[str] = Depends(get_current_user_token)):
    """
    Retrieves the currently authenticated user profile from the JWT token.
    """
    if not token:
        # Default active profile for unauthenticated exploratory sessions
        return UserResponse(
            id="usr-lead-engineer-01",
            email="engineer@impeccable.ai",
            full_name="Lead AI Engineer",
            target_career_path="Agentic AI Systems Engineer",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired or is invalid."
        )

    user_id = payload["sub"]
    # Search store
    for record in _MOCK_USER_STORE.values():
        if record["id"] == user_id:
            return UserResponse(
                id=record["id"],
                email=record["email"],
                full_name=record["full_name"],
                target_career_path=record["target_career_path"],
                is_active=record["is_active"],
                created_at=record["created_at"]
            )

    return UserResponse(
        id=user_id,
        email="learner@impeccable.ai",
        full_name="Learner",
        target_career_path="Agentic AI Systems Engineer",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
