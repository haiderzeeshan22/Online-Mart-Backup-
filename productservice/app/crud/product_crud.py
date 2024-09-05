from typing import Annotated
from fastapi import Depends
from sqlmodel import Session


from app.db import get_session

from app.model import Product


# To Add new Product in Database

async def add_new_product(new_product:Product, session:Session):

    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product



