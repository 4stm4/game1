import cv2, time, os, pysnooper, datetime, pygame
from pygame import camera
from db import SQL
from utils import play_music, do_photo
from pygame import mixer
from flask import Flask, render_template, send_from_directory, redirect, url_for
from buttons import butttons, start_button, buttons_specs, BUTTON
from threading import Thread

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
game_phase = 0  # 0 - ожидание, 1 - старт, 2 игра, 3 - результаты
phase_state = 0 # 0 - init   1 - wait 2 - do it


@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/photo'),filename, mimetype='image')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'),filename, mimetype='audio')

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
    #start_button.sensor._when_activated = 
    return render_template('history.html', rating = history_list)

def start_button_work():
    while True:
        time.sleep(0.2)
        if game_phase == 0:
            if start_button.sensor.is_active:
                gamer_id = SQL('insert','insert_history')
                photo_name = '{}.png'.format(gamer_id)
                t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
                t.start()
                do_photo(photo_name, app.root_path)
                SQL('update', 'update_history',(0, photo_name, gamer_id,))
                return render_template('start.html', foto = '/photo/{}'.format(photo_name))

def buttons_work(): 
    while True:
        time.sleep(0.2)
        for i in butttons:
            if i.sensor.is_active:
                play_music('static/music/button.mp3')
                butttons[i.number].led.off()
                time.sleep(3)
                butttons[i.number].led.on()
                continue

if __name__ == '__main__':    
    app.run(host='127.0.0.1', port=80, debug=True)
    while True:
        time.sleep(0.2)
        if game_phase == 0:
            if phase_state == 0:
        
                for number in range( len(buttons_specs)):
                    butttons.append(BUTTON(number, *buttons_specs[number]))
                    butttons[number].led.on()
                    start_button.led.blink()
                ob_work = Thread(target=buttons_work)
                ob_work.start()
                phase_state = 1
            if phase_state == 1:
                if start_button.sensor.is_active:
                    gamer_id = SQL('insert','insert_history')
                    photo_name = '{}.png'.format(gamer_id)
                    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
                    t.start()
                    do_photo(photo_name, app.root_path)
                    SQL('update', 'update_history',(0, photo_name, gamer_id,))
                    render_template('start.html', foto = '/photo/{}'.format(photo_name))
                    phase_state = 2
        if game_phase == 1:
            pass
        if game_phase == 2:
            pass
        if game_phase == 3:
            pass