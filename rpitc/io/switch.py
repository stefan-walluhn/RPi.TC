from rpitc.io import IO

class Switch(object):

    def __init__(self, out, status = IO.OFF):
        self.out = out
        self.status = status

    def on(self):
        if self.status==IO.OFF:
            self.status = IO.ON
            self.out.trigger()

    def off(self):
        if self.status==IO.ON:
            self.status = IO.OFF
            self.out.trigger()

    def toggle(self):
        if self.status==IO.OFF:
            self.on()
        else:
            self.off()
