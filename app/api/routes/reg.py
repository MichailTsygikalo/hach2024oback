from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from app.core.db import get_session, Session
from app.api.src import try_registration
from app.api.schema import UserReg
router = APIRouter()

@router.post('/')
def registr(user: UserReg, session:Session = Depends(get_session)):
    return try_registration(user,session)