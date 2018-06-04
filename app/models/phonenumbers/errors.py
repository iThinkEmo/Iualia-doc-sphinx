class PhoneNumberError(Exception):
    def __init__(self, message):
        self.message = message



class NumberifyAcessTokenNotFound(PhoneNumberError):
    pass
