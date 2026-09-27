"""
VerifyKE database models.

This file defines the structure of the main database tables
using SQLAlchemy ORM models.

Phase 1 contains three core entities:
- User
- Entity
- Report
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

class Base(DeclarativeBase):
    """
    Base class for all VerifyKE database models.

    SQLAlchemy uses this class to keep track of the models
    that belong to our database.
    """
    pass

class User(Base):
    """
    Represents a person who has an account on VerifyKE.
    """
    __tablename__ = "users"

    # Primary key that uniquely identifies the user.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # User's display name.
    name: Mapped[str] = mapped_column(String(100))
    # User's email address.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    #secure password with password hash
    password_hash: Mapped[str] = mapped_column(String(255))
    # Defines what the user is allowed to do. 
    role: Mapped[str] = mapped_column(String())# "user" and "admin".
    # When the account was created.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,)

    # Relationship to reports submitted by this user.
    reports: Mapped[list["Report"]] = relationship(back_populates="user")


class Entity(Base):
    """
    Represents the phone number, website, business, or other
    identifier that a report is about.
    """
    __tablename__ = "entities"
    
    #unique db ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Type of entity eg. phone, website, business, social-media
    entity_type: Mapped[str] = mapped_column(String(50),)
    # The actual identifier being reported eg. 0712345678, exapmle.com
    value: Mapped[str] = mapped_column(String(500), index=True)
    # When the entity was created.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,)

    # Relationship to reports associated with this entity.
    reports: Mapped[list["Report"]] = relationship(back_populates="entity")


class Report(Base):

    """
    Represents a user-submitted report about a potentially
    fraudulent or suspicious entity.
    """
    __tablename__ = "reports"

    #unique db ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    #Short title describing the report
    title: Mapped[str] = mapped_column(String(200))
    # Detailed description of what happened.
    description: Mapped[str] = mapped_column(Text)
    # Category of the suspected scam eg. "job_scam", "investment_scam", "online_store", "impersonation"
    category: Mapped[str] = mapped_column(String(100))
     # Current review state of the report. New reports start as "pending".
    status: Mapped[str] = mapped_column(String(50), default="pending")
    # ID of the user who submitted the report.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # ID of the entity the report concerns.
    entity_id: Mapped[int] = mapped_column(ForeignKey("entities.id"))
    # When the report was submitted
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,)

    # Relationship back to the user.
    user: Mapped["User"] = relationship(back_populates="reports")

    # Relationship back to the entity.
    entity: Mapped["Entity"] = relationship(back_populates="reports")

