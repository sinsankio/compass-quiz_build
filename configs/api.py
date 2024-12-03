from fastapi import APIRouter

PROJECT_TITLE = "compass"
VERSION = "v1"
MODULE = "api/quizbuild"


def get_base_router(title: str = PROJECT_TITLE, version: str = VERSION, module: str = MODULE) -> APIRouter:
    return APIRouter(prefix=f"/{title}/{version}/{module}")
