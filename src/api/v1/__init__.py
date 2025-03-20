from fastapi import APIRouter

from api.v1 import auth, routes

router = APIRouter(prefix="/api/v1")

router.include_router(routes.router)
router.include_router(auth.router)
