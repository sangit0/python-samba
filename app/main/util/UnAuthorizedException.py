from werkzeug.exceptions import HTTPException


class UnauthorizedException(HTTPException):
    code = 405
    description = 'Unauthorized role is trying to access'