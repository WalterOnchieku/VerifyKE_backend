"""
VerifyKE user schemas.

This file defines the data structures used when users
register, log in, and receive user information from the API.

Schemas control what data is accepted by the API and
what data is returned to the client.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    """
    Data required when creating a new user account.
    """
    # user's display name'
    name: str

    # The user's email address
    # EmailStr makes Pydantic validate that this looks
    # like a valid email address.
    email: EmailStr

    # The plain-text password supplied during registration.
    #
    # Important:
    # This password will NOT be stored directly in the database.
    # It will later be converted into a secure password hash.
    password: str


class UserResponse(BaseModel):
    """
    Data returned by the API when we send user information
    back to the frontend.
    """

    # The user's database ID.
    id: int

    # The user's display name.
    name: str

    # The user's email address.
    email: EmailStr

    # The user's role.
    role: str

    # When the account was created.
    created_at: datetime

    # Allow this schema to work with SQLAlchemy model objects.
    model_config = ConfigDict(
        from_attributes=True,
    )