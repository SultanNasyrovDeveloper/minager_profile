from typing import Annotated

from fastapi import Depends, FastAPI, Request


def get_request_app(request: Request) -> FastAPI:
    return request.app


App = Annotated[FastAPI, Depends(get_request_app)]
