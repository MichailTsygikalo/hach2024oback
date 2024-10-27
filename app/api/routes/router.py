from fastapi import APIRouter

from app.api.routes.reg import router as r
from app.api.routes.product import router as p
from app.api.routes.auth import router as a

router = APIRouter()

router.include_router(r, prefix='/registration', tags=['Регистрация'])
router.include_router(a,prefix='',tags=['Авторизация'])
router.include_router(p, prefix='/product',tags=['Продукты'])
