class PaymentException(Exception):
    def __init__(self, message):
        self.message = message


class PaymentFailedException(PaymentException):
    pass
