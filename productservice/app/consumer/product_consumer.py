from aiokafka import AIOKafkaConsumer


from app.crud import prod_pb2
from app.db import get_session
from app.crud.product_crud import add_new_product
from productservice.app.model import Product



async def productservice_kafkaconsumer(
        topic,
        bootstrapserver
):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrapserver,
        group_id="my-product-consumer-group"
        
    )

    await consumer.start()
    try:
        async for messages in consumer:
            print("Raw")
            print(f"Recieved message on topic {messages.topic}")
            new_product = prod_pb2.Product()
            new_product.ParseFromString(messages.value)

            # to save product in database
            with next(get_session()) as session:
                insert_product_in_db = add_new_product(
                    new_product=Product(**new_product), session=session
                )
                print("insert_product_in_db", insert_product_in_db)



    finally:
        await consumer.stop()      