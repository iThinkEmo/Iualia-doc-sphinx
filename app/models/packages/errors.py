class PackageError(Exception):
    def __init__(self, message):
        self.message = message


class PackageNotFoundError(PackageError):
    pass


class NotEnoughBalanceToSendPackageError(PackageError):
    pass