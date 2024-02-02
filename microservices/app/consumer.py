import os
import pika
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

url = os.environ.get('URL_CLOUD_AMQP')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes incresed!')



channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('Started Consuming')
channel.start_consuming()
channel.close()