from flask import Flask

app = Flask(__name__)
with app.app_context():
    app.config.from_pyfile('config.ini')
    file_db = app.config['DBASE']
    led_delay = app.config['SET_E']
    game_time = app.config['SET_R']
    result_time = app.config['SET_P']
    start_sound = app.config['SET_X']
    end_sound = app.config['SET_Z']
    press_sound = app.config['SET_Y']
    press_delay = app.config['SET_Y']
