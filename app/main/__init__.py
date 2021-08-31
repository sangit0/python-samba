from flask import Flask, request
from flask_cors import CORS

from .config import config_by_name
import logging
from .logger.LogModule import logger
from datetime import datetime as dt


def create_app(config_name):
    app = Flask(__name__)
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:8000",
                    "http: // localhost", "http://127.0.0.1:8000", "http://127.0.0.1:5000", "http://127.0.0.1"]}}, )
    
    app.config.from_object(config_by_name[config_name])

    logger.init_app(app)

    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        log = logging.getLogger("app.access")
        log.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

    return app
