from profile.core.dependencies import App

from fastapi import APIRouter
from sqlalchemy import select, update

from . import models, schemas

router = APIRouter(prefix="/user-profile/profiles")


@router.get("/")
async def list_(
    app: App, page: int = 1, per_page: int = 10
) -> list[schemas.UserProfileSchema]:
    query = select(models.UserProfile).limit(per_page).offset(per_page * (page - 1))
    async with app.state.db.begin() as session:
        results = await session.scalars(query)
    return results


@router.get("/{user_id}")
async def get(user_id: str, app: App) -> schemas.UserProfileSchema:
    async with app.state.db.begin() as session:
        user_profile = await session.get(models.UserProfile, user_id)
    return schemas.UserProfileSchema.model_validate(user_profile)


@router.patch("/{user_id}")
async def patch(
    user_id: str, app: App, data: schemas.UserProfileEditSchema
) -> schemas.UserProfileSchema:
    query = (
        update(models.UserProfile)
        .where(models.UserProfile.user_id == user_id)
        .values(data.model_dump(mode="json", exclude_unset=True, exclude_defaults=True))
        .returning(models.UserProfile)
    )
    async with app.state.db.begin() as session:
        result = await session.scalar(query)
    return result
