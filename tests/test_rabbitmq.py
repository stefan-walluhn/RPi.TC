from rpitc.adapter.rabbitmq import RabbitMQAdapter
import pika
import pytest


@pytest.fixture(scope='session')
def rabbit_connection(mock):
    channel = mock()
    channel.basic_publish = mock()

    connection = mock
    connection.channel = mock(return_value=channel)

    pika.BlockingConnection = connection


@pytest.fixture(scope='session')
def rabbit_adapter(rabbit_connection):
    return RabbitMQAdapter()


class TestRabbitMQAdapter:

    def test_publish(self, rabbit_adapter):
        rabbit_adapter.publish('foo')
        rabbit_adapter.channel.basic_publish.assert_called_once_with(
            body='foo', routing_key='status', exchange='')
