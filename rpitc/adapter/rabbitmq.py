from rpitc.adapter import Adapter
import pika


class RabbitMQAdapter(Adapter):

    def __init__(self):
        connection = pika.BlockingConnection(
                pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='status')

    def publish(self, msg):
        self.channel.basic_publish(
            exchange='', routing_key='status', body=msg)



