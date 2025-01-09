from kafka import KafkaProducer , KafkaConsumer


producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Using
for i in range(10):
    future = producer.send('test-topic', key=str(i).encode(), value=f"message {i}".encode())
    
producer.flush()
producer.close()

conf = {

    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = KafkaConsumer(
    'test-topic', 
    bootstrap_servers='localhost:9092', 
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
