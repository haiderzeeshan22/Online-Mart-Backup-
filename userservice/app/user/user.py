from app.model import RegisterUser, User
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from app.db import get_session
from app.auth import get_user_from_db, hash_password, oauth2_scheme, to_decode_token, current_user


user_router = APIRouter()

@user_router.post("/registerUser")
async def reg_user(newuser:Annotated[RegisterUser, Depends()],
                   session:Annotated[Session, Depends(get_session)]):
    
    db_user = get_user_from_db(session , newuser.username, newuser.email)
    if db_user:
        HTTPException(status_code=404, detail="user with these credentials already exists")

    user = User(username= newuser.username,
                email= newuser.email,
                password= hash_password(newuser.password)
                )    

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message":f"User with {user.username} is added successfully"}


@user_router.get("/profile-login")
async def profile_me(current_user:Annotated[str, Depends(current_user)]):
    
    return current_user
