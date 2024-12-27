from profile.settings import ApplicationSettings

import uvicorn

if __name__ == "__main__":
    settings = ApplicationSettings()
    uvicorn.run(
        "profile.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.logging.level,
        log_config=settings.logging.to_uvicorn_config(),
    )
