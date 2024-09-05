from app.model import TokenData, User
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.db import get_session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime


ALGORITHIM = 'HS256'
SECRET_KEY = "A VERY SECURE SECRET KEY"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes="bcrypt")



def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plainpassword, hash_password):
    return pwd_context.verify(plainpassword, hash_password)



def get_user_from_db(
        session:Annotated[Session, Depends(get_session)],
        username:str | None = None, 
        email: str | None = None
):
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:        
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            return user    
    return user
    
def authenticate_user(        
        username,
        password,
        session:Annotated[Session, Depends(get_session)]
):
    user_in_db = get_user_from_db(session=session, username=username)
    if not user_in_db:
        return False
    if not verify_password(plainpassword=password, hash_password=user_in_db.password):
        return False
    return user_in_db


def create_access_token(subject:str, expiry_time: timedelta):

    expire = datetime.utcnow() + expiry_time

    encode_token = {"exp": expire, "sub":str(subject)}

    access_token = jwt.encode(encode_token, SECRET_KEY, algorithm=ALGORITHIM)

    return access_token



def to_decode_token(access_token:str):
    decode_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHIM] )
    return decode_token   



    
def current_user(token:Annotated[str, Depends(oauth2_scheme)],   # k mera jo current user aagay wo wahi user hai jis sy token bana hai
                 session:Annotated[Session, Depends(get_session)]
                 ):
    credentail_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token please try again",
        headers={"www-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        username = payload.get("sub")   # username ko hum ny "sub" mai save kia tha
        if username is None:
            raise credentail_exception
        token_data = TokenData(username=username)
    except:
        raise JWTError

    user = get_user_from_db(session, username=token_data.username)   
    if not user:
        raise credentail_exception
    return user 

    


