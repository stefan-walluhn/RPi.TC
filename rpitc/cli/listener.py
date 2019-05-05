import click
import logging
from fysom import FysomError

from rpitc.adapter.rabbitmq import RabbitMQAdapter
from rpitc.exceptions import PathCollisionError
from rpitc.layout import layout_factory


@click.command()
@click.option('-l', '--layout', 'layout_src', required=True)
def listen(layout_src):
    # XXX refactor me
    def trail_callback(name):
        try:
            trail = layout.trails[name]
            logging.debug(
                'Handle callback in trail: {} {}'.format(name, trail))
        except KeyError:
            logging.error('Unknown trail: {}'.format(name))
            return False

        try:
            trail.register()
        except PathCollisionError:
            logging.error('Path collission detected: {}'.format(name))
            return False
        except FysomError as e:
            logging.error('{}: {}'.format(str(e), name))
            return False


        trail.activate()

    logging.basicConfig(level=logging.INFO)

    layout = layout_factory.from_file(layout_src)
    layout.setup()

    mq = RabbitMQAdapter(trail_callback=trail_callback)
    mq.run()
