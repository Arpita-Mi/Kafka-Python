import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from config.config import settings

async def produce():
    # Create Kafka producer
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        for i in range(10):
            key = str(i).encode()
            value = f"message {i}".encode()
            await producer.send_and_wait(settings.TOPIC_NAME, key=key, value=value)
            print(f"Sent message {i} to test-topic")
    finally:
        await producer.stop()


async def consume():
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        settings.TOPIC_NAME, 
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id='my-group',  # Consumer group ID
        auto_offset_reset='earliest'  # Start reading from the earliest message if no offset is found
    )
    await consumer.start()

    try:
        while True:
            # Poll messages asynchronously
            async for message in consumer:
                print(f"Received message: {message.value.decode('utf-8')} "
                      f"from partition {message.partition} and offset {message.offset}")
    except asyncio.CancelledError:
        print("Consumer task was cancelled")
    finally:
        await consumer.stop()


async def main():
    producer_task = asyncio.create_task(produce())
    consumer_task = asyncio.create_task(consume())

    # Wait for producer to finish sending messages
    await producer_task
    # Allow the consumer to process for a while before stopping
    await asyncio.sleep(5)
    consumer_task.cancel()  # Cancel the consumer task


if __name__ == '__main__':
    asyncio.run(main())
