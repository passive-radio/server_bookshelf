#app.logger.py

from flask import request
from functools import wraps
from app import app

def http_request_logging(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            app.logger.info('%s - %s - %s - %s', request.remote_addr, request.method, request.url, request.query_string)
        except Exception as e:
            app.logger.exception(e)
            pass
        return f(*args, **kwargs)
    return decorated_function