class ScriptException(Exception):
    def __init__(self, message):
        self.message = message


class ScriptNotFoundException(ScriptException):
    pass