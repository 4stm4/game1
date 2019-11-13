import cv2, time, os, pysnooper, datetime, pygame
from db import SQL
from pygame import mixer
from flask import Flask, render_template, send_from_directory, redirect, url_for
from buttons import butttons, start_button, buttons_specs, BUTTON
from threading import Thread
from webbrowser import open_new

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
game_phase = 0  # 0 - ожидание, 1 - старт, 2 игра, 3 - результаты
active_button = -1


@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/photo'),filename, mimetype='image')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'),filename, mimetype='audio')

@app.route('/game')
def game():
    for button in butttons:
        button.led.off()
    start_button.led.off()
    return render_template('game.html')

@app.route('/')
def index():
    global game_phase
    game_phase = 0
    for button in butttons:
        button.led.on()
    start_button.led.blink()
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

def do_photo(name, path):
    cap = cv2.VideoCapture(0) # Включаем первую камеру
    for i in range(30): cap.read() # "Прогреваем" камеру, чтобы снимок не был тёмным 
    ret, frame = cap.read() # Делаем снимок 
    #frame = frame[300, 150] обрезать фото
    photo_file = '{}/{}'.format(os.path.join(path, 'static/photo'),name)
    cv2.imwrite(photo_file, frame) # Записываем в файл
    cap.release() # Отключаем камеру
    return ''

def play_music(mp3_file:str):
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()


@app.route('/start')
def start_game():
    for button in butttons:
        button.led.off()
    start_button.led.off()
    gamer_id = SQL('insert','insert_history')
    photo_name = '{}.png'.format(gamer_id)
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    do_photo(photo_name, app.root_path)
    SQL('update', 'update_history',(0, photo_name, gamer_id,))
    for button in butttons:
        button.led.on()
    start_button.led.on()
    return render_template('start.html', foto = '/photo/{}'.format(photo_name))

@app.route('/get_game_phase', methods=['POST'])
def get_game_phase():
    return str(game_phase)

def start_button_work():
    global game_phase
    while True:
        time.sleep(0.2)
        if start_button.sensor.is_active:
            game_phase = 1
            break

def buttons_work(): 
    while True:
        time.sleep(0.2)
        if game_phase == 0:
            for i in butttons:
                if i.sensor.is_active:
                    play_music('static/music/button.mp3')
                    butttons[i.number].led.off()
                    time.sleep(3)
                    butttons[i.number].led.on()
                    continue
        else:
            if game_phase ==2:
                pass

if __name__ == '__main__':
    for number in range( len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
    st_work = Thread(target=start_button_work)
    st_work.start()
    ob_work = Thread(target=buttons_work)
    ob_work.start()
    app.run(host='127.0.0.1', port=80, debug=True)
    open_new('127.0.0.1')