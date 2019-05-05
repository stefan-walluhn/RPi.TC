import logging
import pika
from rpitc.adapter import Adapter


logger = logging.getLogger(__name__)


class RabbitMQAdapter(Adapter):

    def __init__(self, trail_callback=None):
        self.trail_callback = self._not_implemented
        if trail_callback:
            self.trail_callback = trail_callback

        connection = pika.BlockingConnection(
                pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='status')
        self.channel.queue_declare(queue='trail')
        self.channel.basic_consume(queue='trail',
                                   auto_ack=True,
                                   on_message_callback=self.trail)

    def publish(self, msg):
        self.channel.basic_publish(
            exchange='', routing_key='status', body=msg)

    def trail(self, ch, method, properties, body):
        logger.info("Trail received {}".format(body))
        self.trail_callback(body.decode('utf-8'))

    def run(self):
        logger.info("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def _not_implemented(self, *args, **kwargs):
        raise NotImplementedError
