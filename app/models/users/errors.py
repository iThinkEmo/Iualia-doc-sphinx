class UserException(Exception):
    def __init__(self, message):
        self.message = message


class UserNotFoundException(UserException):
    pass


class UserAlreadyRegisteredError(UserException):
    pass
