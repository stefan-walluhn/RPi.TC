class PathCollisionError(Exception):

    def __init__(self, value, colliding_trail):
        super(PathCollisionError, self).__init__(value)
        self.colliding_trail = colliding_trail


class SectionBlockedError(Exception):
    pass
