from kafka import KafkaProducer , KafkaConsumer
from config.config import settings

producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)

# Using
for i in range(10):
    future = producer.send(settings.TOPIC_NAME, key=str(i).encode(), value=f"message {i}".encode())
    
producer.flush()
producer.close()

conf = {

    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = KafkaConsumer(
    settings.TOPIC_NAME, 
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, 
    group_id='my-group', 
    auto_offset_reset='earliest'  # Start reading from the earliest message if no offset is found
)


try:
    while True:
        msg = consumer.poll(timeout_ms=1.0)
        if msg is None:
            print("no msg found")
            continue
        if msg.error():
            raise (msg.error())
        for topic_partition, messages in msg.items():
            print(f"Messages for {topic_partition}:")
            for message in messages:
                # Print message key, value, and partition
                print(f"Received message: {message.value.decode('utf-8')}")

except KeyboardInterrupt:
    print("keyboard interuupted")
finally:
    consumer.close()
