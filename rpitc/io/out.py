from rpitc.io import IO
import RPi.GPIO as GPIO

class Out(object):
    status = IO.OFF
    pin = 0

    def __init__(self, pin, status=IO.OFF):
        self.pin = pin
        self.status = status
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        if status==IO.ON:
            self.on()

    def on(self):
        self.status = IO.ON
        GPIO.output(self.pin, IO.ON)

    def off(self):
        self.status = IO.OFF
        GPIO.output(self.pin, IO.OFF)

    def toggle(self):
        if self.status==IO.OFF:
            self.on()
        else:
            self.off() 

