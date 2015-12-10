from rpitc.adapter import Adapter
import pika


class RabbitMQ(Adapter):

    def __init__(self):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='status')

    def update(self, event):
        self.channel.basic_publish(
            exchange='',
            routing_key='status',
            body='test')



