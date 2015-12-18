class PathCollisionError(Exception):

    def __init__(self, value, colliding_path):
        super(PathCollisionError, self).__init__(value)
        self.colliding_path = colliding_path
