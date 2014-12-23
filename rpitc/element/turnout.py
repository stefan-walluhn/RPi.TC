class Turnout:
    
    STRAIGHT = 0
    TURNOUT = 1

    status = None

    def switch(self, direction):
        if self.status == direction:
            return
        self.status = direction
