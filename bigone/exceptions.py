class BigoneRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'BigoneRequestException: %s' % self.message

class BigoneAPIException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'BigoneAPIException(code=%s): %s' % (self.code, self.message)
