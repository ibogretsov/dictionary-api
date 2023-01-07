from fastapi import APIRouter

from app.api import words


api_router = APIRouter(prefix='/api')
api_router.include_router(router=words.router)
