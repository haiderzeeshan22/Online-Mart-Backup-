from fastapi import FastAPI, Depends, HTTPException, Form
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, select, create_engine, Field
from typing import Annotated



class User(SQLModel, table=True):
    id : int = Field(default=None , primary_key= True)
    username: str
    email : str
    password : str


class RegisterUser(BaseModel):
    username:Annotated[
        str,
          Form()
    ]
    email:Annotated[
        str,
          Form()
    ]
    password:Annotated[
        str,
          Form()
    
    ]



class Token(BaseModel):
    access_token :str
    token_type : str
    # refresh_token:str


class TokenData(BaseModel):
    username: str