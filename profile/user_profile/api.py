from fastapi import APIRouter

router = APIRouter(prefix="/user-profile/profiles")


@router.get("/")
async def profiles():
    return []
