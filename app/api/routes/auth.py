"""
VerifyKE authentication API routes.

This file contains endpoints for:

- Registering new users.
- Logging existing users in.

Passwords are never stored directly in the database.
They are converted into secure password hashes first.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse

# Create a router for authentication endpoints
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

# Algorithm used to sign our JWT tokens.
ALGORITHM = "HS256"

# How long a login token remains valid
ACCESS_TOKENS_EXPIRE_MINUTES=60


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new VerifyKE user.

    The supplied password is hashed before the user
    is saved to the database.
    """
    # Check whether an account with this email already exists
    result = await db.execute(
        select(User).where(
            User.email==user_data.email
        )
    )

    existing_user = result.scalar_one_or_none()

    # Do not allow duplicate email addresses
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "An account with this email already exists"
        )

    # Convert the plain-text password into a secure hash
    password_hash = hash_password(
        user_data.password
    )

    # Create the SQLAlchemy User object
    user = User(
        name=user_data.name,
        email = user_data.email,
        password_hash = password_hash,
        role = "user"
    )

    # Add the user to the database session
    db.add(user)

   # Save the new user
    await db.commit()

    # Refresh the object so generated fields such as
    # the database ID are available
    await db.refresh(user)

    # Return the user using UserResponse.
    #
    # UserResponse does NOT contain password_hash
    return user

@router.post("/login")

async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate a user and return a JWT access token.

    FastAPI's OAuth2PasswordRequestForm expects:

    username = user's email
    password = user's password
    """
    # Find the user by email
    result = await db.execute(
        select(User).where(
            User.email == form_data.username
        )
    )

    user = result.scalar_one_or_none()

    # If the account doesn't exist, authentication fails
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Compare the supplied password with the stored hash
    password_is_valid = verify_password(
        form_data.password,
        user.password_hash,
    )

    # Reject incorrect passwords
    if not password_is_valid:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )

    # Create the token payload
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKENS_EXPIRE_MINUTES)
    }

   # Sign the JWT using our application's secret key
    access_token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm = ALGORITHM,
    ) 

    # Return the token to the frontend
    return{
        "access_token": access_token,
        "token_type": "bearer",
    }