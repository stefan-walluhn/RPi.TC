class Turnout(object):
    STRAIGHT = True
    TURNOUT = False

    def __init__(self, status=None):
        if status is None:
            self.status = self.STRAIGHT
        else:
            self.status = status

    def switch(self, direction):
        if self.status == direction:
            return
        self.status = direction
