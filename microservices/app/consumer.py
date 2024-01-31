import os
import pika

url = os.environ.get('URL_CLOUD_AMQP')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback)
print('Started Consuming')
channel.start_consuming()
channel.close()