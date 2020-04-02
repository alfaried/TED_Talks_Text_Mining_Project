import os

SECRET_KEY = 'not so secret'
TEMPLATES_AUTO_RELOAD = True
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(SITE_ROOT, '/app/upload')