from profile.core.utils import make_database_url
from profile.settings import ApplicationSettings
from profile.user_profile.api import router as user_profile_router

from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

app = FastAPI()
settings = ApplicationSettings()
engine = create_async_engine(make_database_url(settings.db), echo=True)
db = async_sessionmaker(engine, expire_on_commit=False)
app.state.db = db

v1_router = APIRouter(prefix="/api/v1")


@v1_router.get("/healthcheck")
async def healthcheck() -> str:
    return "Ok"


v1_router.include_router(user_profile_router, tags=["User Profile"])

app.include_router(v1_router)
