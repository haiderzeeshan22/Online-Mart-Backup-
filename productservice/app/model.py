from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field
from pydantic import UUID4



class Product(SQLModel, table=True):
    id : UUID4 =  Field(default_factory=uuid4, primary_key=True, index=True)
    name : str = Field(index=True, max_length=54)
    description : str = Field(default=None, max_length=500)
    price : int = Field(nullable=False)
    stock : int = Field(default=0)
    is_active : bool = Field(default=True)
    category_id : int = Field(foreign_key="category.id")


class category(SQLModel, table=True):
    id: int= Field(default_factory=uuid4, index=True, primary_key=True)
    name : str = Field(index= True, nullable=False, unique=True, max_length=100)
    description : Optional[str] = Field(default=None, max_length=255)

    