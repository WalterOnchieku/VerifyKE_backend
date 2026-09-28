"""
VerifyKE FastAPI application entry point.

This file creates the main FastAPI application
and registers all API routers.

The routers contain the actual endpoints for:

- Authentication
- Entities
- Reports
"""

from fastapi import FastAPI

from app.api.routes import auth, entities, reports, admin

# CREATE FASTAPI APPLICATION

app = FastAPI(
    title="VerifyKE API",
    description=(
        "API for reporting and checking potentially "
        "fraudulent entities in Kenya."
        ),
    version="1.0.0",
)


# REGISTER API ROUTERS

# Authentication endpoints.
# Available under: /auth/...
app.include_router(auth.router)

# Entity endpoints.
# Available under: /entities/...
app.include_router(entities.router)

# Report endpoints.
# Available under: /reports/...
app.include_router(reports.router)

# Admin endpoints.
# Available under: /admin/...
app.include_router(admin.router)

# BASIC APPLICATION ENDPOINTS

@app.get("/")
async def root():
    """
    Basic endpoint confirming that the VerifyKE API is running.
    """
    return {
        "message": "VerifyKE API is running."
    }


@app.get("/health")
async def health_check():
    """
    Health-check endpoint.

    This can later be used by Docker, cloud platforms,
    monitoring systems, or load balancers to check whether
    the API is alive.
    """
    return {
        "status": "Healthy"
    }