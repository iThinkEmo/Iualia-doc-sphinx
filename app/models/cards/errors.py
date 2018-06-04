class CardException(Exception):
    def __init__(self, message):
        self.message = message


class CardNotFoundException(CardException):
    pass


class TokenizationFailedException(CardException):
    pass


class RepeatedCardException(CardException):
    pass
