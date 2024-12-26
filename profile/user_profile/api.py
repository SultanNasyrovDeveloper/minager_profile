from fastapi import APIRouter

router = APIRouter(prefix="/user-profile/profiles")


@router.get("/")
async def list_():
    return []


@router.get("/{id_}")
async def get(id_: int):
    pass


@router.patch("/{id_}")
async def patch(id_: int, data: dict):
    pass
