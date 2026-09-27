"""
VerifyKE report API routes.

This file contains HTTP endpoints related to reports.

The route receives requests from the frontend,
validates the incoming data using Pydantic schemas,
identifies the authenticated user,
calls the report service, and returns the result.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.schemas.report import ReportCreate, ReportResponse
from app.services.report_service import create_report

# Create a router for report-related endpoints.
router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

@router.post(
    "/",
    response_model=ReportResponse,
    )

async def submit_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a new report.

    The current user is obtained from the JWT access token.

    This means users can only submit reports while authenticated.
    """
    # Temporary user ID for development.
    #
    # Later this will come from the authenticated user.

    # current_user_id = 1

    try:
        # Send the validated report data to the service layer.
        #
        # Instead of using a hard-coded user ID,
        # we use the ID of the authenticated user.
        report = await create_report(
            db=db,
            report_data=report_data,
            user_id=current_user.id,
        )

        # Return the newly created report
        return report

    except ValueError as error:
        # Convert our service-level error into
        # a proper HTTP 404 response
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )