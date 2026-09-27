"""
VerifyKE report schemas.

This file defines the data structures used when users
submit reports and when report information is returned
by the API.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ReportCreate(BaseModel):
    """
    Data required when a user submits a new report.
    """
    # Short title describing the incident.
    #
    # Example:
    # "Fake job offer"
    title: str

    # Detailed explanation of what happened.
    description: str

    # Category of the suspected scam.
    #
    # Examples:
    # "job_scam"
    # "investment_scam"
    # "online_store"
    # "impersonation"
    category: str

    # ID of the entity that the report concerns.
    #
    # For example, if the report concerns phone number
    # 0712345678 and that phone number has ID 12,
    # entity_id would be 12.
    entity_id: int


class ReportResponse(BaseModel):
    """
    Data returned by the API when sending report information
    back to the frontend.
    """
    # Unique report ID.
    id: int

    # Short report title.
    title: str

    #Detailed description
    description: str

    #scam category
    category: str

    # Current moderation/review status.
    #
    # Example:
    # "pending"
    # "verified"
    # "rejected"

    status: str

    # ID of the user who submitted the report.
    user_id: int

    # ID of the entity being reported.
    entity_id: int

    # Time the report was created
    created_at: datetime

    # Allow Pydantic to create this schema from
    # an SQLAlchemy Report object.
    model_config = ConfigDict(
        from_attributes=True,
    )