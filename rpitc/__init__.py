class PathCollision(Exception):

    def __init__(self, value, colliding_trail):
        self.value = value
        self.colliding_trail = colliding_trail

    def __str__(self):
        return repr(self.value)
    
