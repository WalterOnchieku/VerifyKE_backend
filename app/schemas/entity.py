"""
VerifyKE entity schemas.

This file defines the data structures used when entities
are created, searched for, or returned by the API.

An entity represents something that users can report,
such as a phone number, website, business, or social media account.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

class EntityCreate(BaseModel):

    """
    Data required when creating a new entity.
    """
    # The type of entity being reported.
    #
    # Examples:
    # "phone"
    # "website"
    # "business"
    # "social_media"
    entity_type: str

    # The actual identifier of the entity.
    #
    # Examples:
    # "0712345678"
    # "example.com"
    # "@example_store"
    value: str

class EntityResponse(BaseModel):
    """
    Data returned by the API when sending entity information
    back to the frontend.
    """
    # The entity's database ID.
    id: int

    # The type of entity.
    entity_type: str

    # The actual value being reported
    value: str

    # When the entity was created.
    created_at: datetime

    # Allow this schema to work with SQLAlchemy model objects.
    model_config = ConfigDict(
            from_attributes=True,
        )
