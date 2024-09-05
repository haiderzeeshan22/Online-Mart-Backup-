from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select, create_engine, Field
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.user import user
from app.auth import authenticate_user, create_access_token, get_user_from_db, to_decode_token, oauth2_scheme
from app.db import get_session, create_table
from contextlib import asynccontextmanager
from datetime import timedelta
from app.model import Token
from jose import JWTError


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("creating tables")
    create_table()
    yield



app = FastAPI(lifespan=lifespan)
app.router.include_router(user.user_router)



@app.get("/")
async def root():
    return{"Message":"this is User Service"}



# @app.post("/token", response_model=Token)
# async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
#                 session:Annotated[Session, Depends(get_session)]
#                 ):
#     user = authenticate_user( form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(status_code=404, detail="Invalid Username and Password")

#     token_time = timedelta(minutes=15)
#     access_token = create_access_token(subject=form_data.username, expiry_time=token_time)

#     return Token(access_token= access_token, token_type= "bearer")


@app.post("/token", response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                session:Annotated[Session, Depends(get_session)]
                ):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=404, detail="invalid username and password")
    
    token_time = timedelta(minutes= 1)
    access_token = create_access_token(subject=form_data.username, expiry_time=token_time)

    return Token(access_token=access_token, token_type="bearer")




@app.get("/decode_token")
async def decoding_token(access_token:str):
    try:
        decode_token = to_decode_token(access_token)
        return {"decode token": decode_token}
    except JWTError as e :
        return{"error":str(e)}

