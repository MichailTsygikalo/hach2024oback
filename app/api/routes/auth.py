import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.api.schema import UserLogin
from app.models.model import UserModel, pwd_context
from app.core.settings import app_settings
from app.core.db import Session, get_session

SECRET_KEY = app_settings.secret_key
ALGORITHM = app_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload

router = APIRouter()
# pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/token")
def login(form_data: UserLogin, db: Session = Depends(get_session)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    # print(user.password,pwd_context.hash(form_data.password))
    if not user or not user.password == form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id":user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_session)):
    user = db.query(UserModel).filter(UserModel.id == current_user['id']).first()
    return user
