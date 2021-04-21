
class InputValueError(Exception):

    def __init__(self, message):
        self.message = message
