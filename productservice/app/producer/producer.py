from aiokafka import AIOKafkaProducer


# Kafka Producer as a dependency
async def productservice_kafkaproducer(
        
):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    await producer.start()
    try:
        yield producer

    finally:
        await producer.stop()    
        



