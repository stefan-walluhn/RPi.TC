from rpitc.io import IO
import RPi.GPIO as GPIO


class Out(object):

    def __init__(self, pin, status=IO.OFF):
        self.__pin__ = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pin__, GPIO.OUT)
        self._status = self.set_pin(status)

    @property
    def status(self):
        return self._status

    def set_pin(self, status):
        GPIO.output(self.__pin__, status)
        return status

    def on(self):
        self._status = self.set_pin(IO.ON)

    def off(self):
        self._status = self.set_pin(IO.OFF)

    def toggle(self):
        if self.status==IO.OFF:
            self.on()
        else:
            self.off() 

