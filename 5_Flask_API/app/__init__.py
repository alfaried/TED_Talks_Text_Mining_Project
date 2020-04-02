import logging

from flask import Flask

logging.basicConfig(level=logging.INFO,
                    format='[%(filename)s:%(lineno)s | %(funcName)s() | %(asctime)s | %(levelname)s] %(message)s')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_object('config')

from app.views import *

