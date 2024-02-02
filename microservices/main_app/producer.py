import os
import pika
import json

url = os.environ.get('URL_CLOUD_AMQP')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
