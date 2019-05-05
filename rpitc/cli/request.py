import click
import pika


@click.command()
@click.option('-t', '--trail', required=True)
def trail(trail):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='trail')
    channel.basic_publish(exchange='', routing_key='trail', body=trail)
    connection.close()

