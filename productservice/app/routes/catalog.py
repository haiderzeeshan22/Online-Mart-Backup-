from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session, select


from app.model import category
from app.db import get_session


category_router = APIRouter()


@category_router.post("/add-category")
async def add_category(
        new_category:Annotated[category, Depends()],
        session:Annotated[Session, Depends(get_session)]
):
    categori = category(
        id = new_category.id,
        name= new_category.name,
        description=new_category.description
    )
    session.add(categori)
    session.commit()
    session.refresh(categori)
    return{"message":f"category with {category.name} has added successfully"}