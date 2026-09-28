"""
VerifyKE administration API routes.

This file contains endpoints that are restricted
to VerifyKE administrators.

Administrators can:
- View pending reports.
- Verify reports.
- Reject reports.

Normal users cannot access these endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.db.database import get_db
from app.db.models import Report, User
from app.schemas.report import ReportResponse

router = APIRouter(
    prefix="/admin",
    tags=["Administration"]
)


@router.get(
    "/reports/pending",
    response_model=list[ReportResponse]
)

async def get_pending_reports(
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Retrieve all reports that are waiting for review.

    Only administrators can access this endpoint.
    """
    result = await db.execute(
        select(Report).where(
            Report.status == "pending"
        )
        .order_by(
            Report.created_at.desc()
        )
    )

    return result.scalars().all()


@router.patch(
    "/reports/{report_id}/verify",
    response_model=ReportResponse,
)
async def verify_report(
    report_id: int, 
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Mark a pending report as verified.

    Only administrators can perform this action.
    """
    result = await db.execute(
        select(Report).where(
            Report.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.status != "pending":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="only pending reports can be verified"
        )

    report.status = "verified"

    await db.commit()

    await db.refresh(report)

    return report


@router.patch(
    "/reports/{report_id}/reject",
    response_model=ReportResponse,
)
async def verify_report(
    report_id: int, 
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    """
    Mark a pending report as rejected.

    Only administrators can perform this action.
    """
    result = await db.execute(
        select(Report).where(
            Report.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.status != "pending":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="only pending reports can be rejected"
        )

    report.status = "rejected"

    await db.commit()

    await db.refresh(report)

    return report