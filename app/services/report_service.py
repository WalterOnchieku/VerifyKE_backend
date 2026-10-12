"""
VerifyKE report service.

This file contains the business logic related to reports.

The service is responsible for:
- Validating the entity.
- Creating the report.
- Saving the report to PostgreSQL.
- Publishing a report-created event to RabbitMQ.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Entity, Report
from app.schemas.report import ReportCreate
from app.messaging.rabbitmq import publish_event
from app,messaging.events import report_created_event

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
    """
    Create a new report and publish a RabbitMQ event.

    The database transaction is completed before the
    RabbitMQ event is published.
    """

    # STEP 1 — Verify that the entity exists
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

    # Create the RabbitMQ event
    event = report_created_event(
        report_id=report.id,
        user_is=report.user_id,
        entity_id=report.entity_id,
    )

    # Publish the event
    await publish_event(
        queue_name = "report_created",
        event = event,
    )

    # Return the newly created report
    return report