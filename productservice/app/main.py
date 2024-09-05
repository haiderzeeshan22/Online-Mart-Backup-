# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import AsyncGenerator, Annotated
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import asyncio
import json
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError


# from app.model import Product, Category

from app.routes import catalog
from app.db import create_table, get_session
from app.model import Product
from app.producer.producer import productservice_kafkaproducer
from app.crud.product_crud import add_new_product
from app import prod_pb2
from app import settings





# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    
    # task = asyncio.create_task(consume_messages('todos', 'broker:19092'))
    yield

#  Fast API Code 
app = FastAPI(lifespan=lifespan, title="Hello World API with DB", 
    version="0.0.1",
    # servers=[
    #     {
    #         "url": "http://127.0.0.1:8002", # ADD NGROK URL Here Before Creating GPT Action
    #         "description": "Development Server"
    #     },
    #     {
    #         "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
    #         "description": "Development Server"
    #     }
    #     ]
    )

app.router.include_router(catalog.category_router)


@app.get("/")
def read_root():
    return {"App": "Service 2"}




@app.post("/add-product", response_model=Product)
async def create_product(new_product: Product, 
                         session: Annotated[Session, Depends(get_session)], 
                         producer:Annotated[AIOKafkaProducer, Depends(productservice_kafkaproducer)]):
    
    product_protobuf = prod_pb2.Product(
                                           id= new_product.id,
                                           name = new_product.name,
                                           description = new_product.description,
                                           price = new_product.price,
                                           stock= new_product.stock,
                                           is_active= new_product.is_active,
                                           category_id= new_product.category_id
                                           )
    serialize_protobuf = product_protobuf.SerializeToString()
    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, serialize_protobuf)
    return new_product



