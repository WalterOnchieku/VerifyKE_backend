"""
VerifyKE security utilities.

This file contains security-related helper functions.

For Phase 1, we focus on password hashing and password
verification. Authentication tokens will be added when
we build the authentication routes.
"""
"""
VerifyKE security utilities.

This file contains security-related helper functions.

Responsibilities:
- Hash user passwords.
- Verify user passwords.
- Decode and validate JWT access tokens.
- Identify the currently authenticated user.

Authentication routes create JWT tokens.
This file contains the reusable logic for checking those tokens.
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.db.models import User

# Create a password hashing configuration.
# bcrypt is used to securely hash passwords.
# The application will never store the user's actual password in the database.
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    
    """
    Convert a plain-text password into a secure password hash.

    Example:
        password: "mypassword123"
        becomes something similar to: "$2b$12$...."
    """
    return password_hash.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str,
) -> bool:
    """
    Check whether a plain-text password matches
    a previously stored password hash.

    Returns:

        True  -> password is correct
        False -> password is incorrect
    """

    return password_hash.verify(
        plain_password,
        hashed_password,
    )

# JWT CONFIGURATION
# Algorithm used to sign and verify our JWT tokens
ALGORITHM = "HS256"

# Tell FastAPI where clients should obtain their access token.
#
# This is used by the OAuth2PasswordBearer dependency.

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "/auth/login",
)

# JWT DECODING
def decode_access_token(token:str) -> dict:
    """
    Decode and validate a JWT access token.

    The token must:
    - Be correctly signed using our SECRET_KEY.
    - Use the expected algorithm.
    - Contain a valid payload.

    Returns:
        The decoded JWT payload.

    Raises:
        HTTP 401 if the token is invalid.
    """
    try: 
        # Decode the token using our application's secret key
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms = ALGORITHM,
        )

        # The "sub" claim identifies the user.
        user_id = payload.get("sub")

        # A token without a subject cannot identify
        #  the authenticated user.

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "invalid authentication token",
                headers = {
                    "WWW-authenticate": "bearer",
                },
            )
        return payload

    except JWTError:
        # This catches invalid, expired, malformed,
        # or incorrectly signed tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )


# CURRENT USER
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Identify the currently authenticated user.

    The process is:

        HTTP request
            ↓
        Bearer token
            ↓
        Decode JWT
            ↓
        Extract user ID
            ↓
        Find user in database
            ↓
        Return User object
    """
    # Decode and validate the JWT
    payload = decode_access_token(token) 

    # Get the user ID stored in the token
    user_id = payload.get("sub")

    # Convert the user ID from the JWT into an integer
    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid user identifier in token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # Look up the user in PostgreSQL
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    # The token may technically be valid while the
    # corresponding account no longer exists
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user account no longer exists",
            headers={
                "WWW-Authenticate": "Bearer",
            }
        )
    # Return the actual SQLAlchemy User object
    return user

# ADMIN AUTHORIZATION
async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Require the authenticated user to have the admin role.

    Authentication answers:

        "Who are you?"

    Authorization answers:

        "Are you allowed to perform this action?"

    This function handles the second question.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user



    
