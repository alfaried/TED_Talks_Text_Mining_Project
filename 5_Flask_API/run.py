#!flask/bin/python
from app import app

if __name__ == '__main__':
    app.run(host='localhost', port=8088, debug=True, use_reloader=app.config['TEMPLATES_AUTO_RELOAD'])