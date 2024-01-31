import os
import pika

url = os.environ.get('URL_CLOUD_AMQP')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish():
    channel.basic_publish(exchange='', routing_key='admin', body='hello')
