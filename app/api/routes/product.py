from fastapi import APIRouter, Depends

from app.core.db import get_session, Session
from app.api.src import get_product, get_all_product, add_product, drop_product, get_product_e
from app.api.schema import Product
from app.api.routes.auth import get_current_user

router = APIRouter()

@router.get('/product')
def product(id:int, session:Session=Depends(get_session),current_user: dict = Depends(get_current_user)):
    return get_product(id, session)

@router.get('/all_product')
def productall( session:Session=Depends(get_session),current_user: dict = Depends(get_current_user)):
    return get_all_product(current_user['id'], session)

@router.post('/add_product')
def aproduct(product:Product, session:Session=Depends(get_session),current_user: dict = Depends(get_current_user)):
    return add_product(product, session)

@router.post('/drop_product')
def dproduct(p_id:int,c_id:int, session:Session=Depends(get_session),current_user: dict = Depends(get_current_user)):
    return drop_product(p_id,current_user['id'],c_id,session)

@router.get('/product_e')
def producte(id_prod:int,session:Session=Depends(get_session),current_user: dict = Depends(get_current_user)):
    return get_product_e(id_prod,session)