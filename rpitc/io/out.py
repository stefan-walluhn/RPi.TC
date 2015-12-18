from rpitc.io import IO, BaseOut
import RPi.GPIO as GPIO


class Out(BaseOut):

    def __init__(self, pin, status=IO.OFF):
        self.__pin__ = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pin__, GPIO.OUT)
        super(Out, self).__init__(status)

    def set_pin(self, status):
        GPIO.output(self.__pin__, status)
        return status

    def _on(self):
        return self.set_pin(IO.ON)

    def _off(self):
        return self.set_pin(IO.OFF)
