from flask import Flask

app = Flask(__name__)
with app.app_context():
    app.config.from_pyfile('config.ini')
    file_db = app.config['DBASE']