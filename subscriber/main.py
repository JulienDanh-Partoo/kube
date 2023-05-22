from random import randint

import pika
from pika.exchange_type import ExchangeType


# Define the callback function
def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

# Establish connection to RabbitMQ server
credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials))
channel = connection.channel()

# Create an exchange named 'my_exchange' of type 'topic'
channel.exchange_declare(exchange='Business', exchange_type=ExchangeType.fanout)

# Create a queue
result = channel.queue_declare(queue=f'XX_queue_{randint(0,10000)}')
queue_name = result.method.queue
print(queue_name)

# Bind the queue to the exchange with the routing key 'Business.edit'
channel.queue_bind(exchange='Business', queue=queue_name, routing_key='Business.edit')

# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for messages. Press Ctrl+C to exit.")

# Start consuming messages indefinitely
channel.start_consuming()