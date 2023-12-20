from fastapi import APIRouter
from routers import user_router, login_router, image_router


routers = APIRouter()


routers.include_router(login_router.router,    prefix="/login",   tags=["login"])
routers.include_router(user_router.router,     prefix="/user",    tags=["user"])
routers.include_router(image_router.router,     prefix="/image",    tags=["image"])