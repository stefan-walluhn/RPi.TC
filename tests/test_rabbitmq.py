#from rpitc.adapter.rabbitmq import RabbitMQ
#from rpitc.trail import Trail, Event
#
#class TestRabbitMQ:
#
#    rabbit = RabbitMQ()
#
#    def test_init(self):
#        assert isinstance(self.rabbit, RabbitMQ)
#
#    def test_logging(self):
#        trail = Trail()
#        e = Event(trail, src=Trail.IDLE, dst=Trail.ACTIVE)
#        self.rabbit.update(e)
