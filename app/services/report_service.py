"""
VerifyKE report service.

This file contains the business logic related to reports.

The API routes should handle HTTP requests and responses,
while this service handles the actual application logic
for creating and retrieving reports.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Entity, Report
from app.schemas.report import ReportCreate

async def create_report(
        db: AsyncSession,
        report_data: ReportCreate,
        user_id: int,
) -> Report:
    """
    Create a new report in the database.
    Parameters:
        db: Active SQLAlchemy database session.

        report_data: Validated report information received from the API.

        user_id: ID of the authenticated user submitting the report.

    Returns:
        The newly created Report database object.
    """

    # Look for the entity that the report is about.
    #
    # For example, if entity_id is 12, we look for
    # the Entity whose database ID is 12.
    result = await db.execute(
        select(Entity).where(
            Entity.id==report_data.entity_id
            )
    )

    # Get the entity from the query result
    entity = result.scalar_one_or_none()

    # If the entity does not exist, stop the operation
    if entity is None:
        raise ValueError("Entity not found")

    # Create a new Report database object
    report = Report(
        title = report_data.title,
        description = report_data.description,
        category = report_data.category,
        user_id = user_id,
        entity_id = report_data.entity_id
    )

    # Add the new report to the current database session
    db.add(report)

    # Save the changes to PostgreSQL
    await db.commit()

    # Refresh the object so SQLAlchemy loads values generated
    # by the database, such as the new report ID
    await db.refresh(report)

    # Return the newly created report
    return report