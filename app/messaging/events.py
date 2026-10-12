"""
VerifyKE messaging events.

This file defines the events that can be sent through
RabbitMQ.

Keeping event construction in one place helps prevent
different parts of the application from creating
inconsistent messages.
"""
def report_created_event(
        report_id: int,
        user_id: int,
        entity_id: int,
) -> dict:
    """
    Create an event indicating that a new report was created.

    This event will eventually trigger background processing
    such as risk analysis and duplicate detection.
    """
    return {
        "event_type": "report.created",
        "report_id": report_id,
        "user_id": user_id,
        "entity_id": entity_id
    }