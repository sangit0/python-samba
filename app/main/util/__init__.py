from flask_restplus import abort


def make_error(status_code=500, message='Internal Server Error', errors=None):
    abort(status_code, message, errors=errors)
