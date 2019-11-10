import cv2, time, os, pysnooper, datetime
from db import SQL
from utils import do_photo, play_music
from flask import Flask, render_template, send_from_directory
from buttons import butttons, start_button, buttons_specs, BUTTON
from threading import Thread
from SimpleCV import Image, Camera

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
    #do_photo(photo_name, app.root_path)
    cam = Camera()
    img = cam.getImage()
    img.save(photo_name)
    SQL('update', 'update_history',(0, photo_name, gamer_id,))
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    return render_template('start.html', foto = '/photo/{}'.format(photo_name))

def start_button_work():
    cnt = 0 
    while True:
        if start_button.sensor.is_active:
            cnt += 1
            print('start {}'.format(cnt))
            start_game()
            time.sleep(1)
            continue

def buttons_work(): 
    while True:
        for i in butttons:
            if i.sensor.is_active:
                play_music('static/music/button.mp3')
                butttons[i.number].led.off()
                time.sleep(3)
                butttons[i.number].led.on()

                continue

if __name__ == '__main__':
    for number in range( len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
        butttons[number].led.on()
    start_button.led.blink()
    t = Thread(target=start_button_work)
    t.start()
    d = Thread(target=buttons_work)
    d.start()
    buttons_cnt = len(butttons)
    app.run(host='127.0.0.1', port=80, debug=True)