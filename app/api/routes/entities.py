"""
VerifyKE entity API routes.

This file contains endpoints for creating and
searching entities.

An entity represents something that users can report,
such as a phone number, website, business, or
social media account.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import Entity
from app.schemas.entity import EntityCreate, EntityResponse

# Create a router for entity-related endpoints
router = APIRouter(
    prefix="/entities",
    tags=["Entities"],
)


@router.post(
    "/",
    response_model=EntityResponse,
    status_code=status.HTTP_201_CREATED,
)

async def create_entity(
    entity_data: EntityCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new entity.

    If an entity with the same type and value already
    exists, return the existing entity instead of creating
    a duplicate.
    """
    # Look for an existing entity with the same type and value
    result = await db.execute(
        select(Entity).where(
            Entity.entity_type == entity_data.entity_type,
            Entity.value == entity_data.value
        )
    )

    existing_entity = result.scalar_one_or_none()

    # If the entity already exists, return it
    if existing_entity is not None:
        return existing_entity

    # Create a new Entity database object
    entity = Entity(
        entity_type = entity_data.entity_type,
        value = entity_data.value
    )

    # Add the entity to the database session
    db.add(entity)

    # Save the entity
    await db.commit()

    # Refresh the object so the generated ID is available
    await db.refresh(entity)

    # Return the newly created entity
    return entity

@router.get(
    "/entity_id",
    response_model=EntityResponse
)
async def get_entity(
    entity_id:int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve an entity using its database ID.
    """
    # Find the entity by its ID
    result = await db.execute(
        select(Entity).where(
            Entity.id == entity_id
        )
    )

    entity = result.scalar_one_or_none()

    # Return a 404 if the entity doesn't exist
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    return entity

@router.get(
    "/search/{value}",
    response_model=list[EntityResponse],
)
async def search_entities(
    value: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Search for entities using their value.

    Example:

        /entities/search/0712345678

    or:

        /entities/search/example.com
    """
    # Search for entities whose value contains the
    # supplied search term.
    result = await db.execute(
        select(Entity).where(
            Entity.value.ilike(f"%{value}%")
        )
    )

    #return all matching entities
    return result.scalars().all