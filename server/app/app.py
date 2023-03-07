# app.__init__.py
import os

from flask import Flask
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'file': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': './log/test.log',
            'backupCount': 3,
            'when': 'D',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.debug('debug')
    app.logger.info('info')
    app.logger.warn('warn')
    app.logger.error('error')
    app.logger.critical('critical')
    return 'hello'

if __name__ == "__main__":
    app.run(host='0.0.0.0')