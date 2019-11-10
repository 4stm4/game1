import cv2, time, os, pysnooper, datetime
from db import SQL
from utils import do_photo, play_music
from flask import Flask, render_template, send_from_directory
from buttons import butttons, init_buttons, start_button
from selenium import webdriver
from threading import Thread

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
buttons_cnt = 0
game_phase = 0  # 0 - ожидание, 1 - старт, 2 игра, 3 - результаты


@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/photo'),filename, mimetype='image')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'),filename, mimetype='audio')

@app.route('/game1')
def index():
    history_list = []
    responce = SQL('select_all', 'view_history')
    j = 0
    for i in responce:
        j += 1
        history_list.append(
            {
                "num" : j,
                "name": i[0],
                "rslt": i[1],
                "foto": "/static/photo/{}".format(i[2])
            }
        )
    return render_template('history.html', rating = history_list)

@app.route('/start')
def start_game():
    gamer_id = SQL('insert','insert_history', (datetime.datetime.now(),))
    photo_name = '{}.jpeg'.format(gamer_id)
    do_photo(photo_name, app.root_path)
    SQL('update', 'update_history',(0, photo_name, gamer_id, datetime.datetime.now(),))
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    return render_template('start.html', foto = '/photo/{}'.format(photo_name))

if __name__ == '__main__':
    init_buttons()
    buttons_cnt = len(butttons)
    app.run(host='127.0.0.1', port=80, debug=True)
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1/game1')
    driver.maximize_window()