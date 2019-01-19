class AppException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        ret_val = dict(self.payload or ())
        ret_val['error'] = self.message
        return ret_val


class ValidationException(AppException):
    pass


class AuthorizationException(AppException):
    def __init__(self, message, status_code=401):
        super().__init__(message, status_code)


class AdminOnlyException(AuthorizationException):
    def __init__(self, message):
        super().__init__(message, status_code=401)
