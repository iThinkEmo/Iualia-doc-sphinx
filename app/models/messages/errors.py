class MessageErrors(Exception):
    def __init__(self, message):
        self.message = message


class MessageBodyEmpty(MessageErrors):
    pass