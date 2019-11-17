import cv2, time, os, datetime, pygame, random
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
game_points = 0


@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/photo'),filename, mimetype='image')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'),filename, mimetype='audio')

@app.route('/game')
def game():
    global game_phase, game_points
    game_phase = 2
    for button in butttons:
        button.led.off()
    start_button.led.off()
    return render_template('game.html')

@app.route('/game_over')
def game_over():
    global game_phase, game_points
    game_phase = 3
    for button in butttons:
        button.led.blink()
    start_button.led.blink()
    return render_template('game_over.html')

@app.route('/')
def index():
    global game_phase, game_points
    game_phase = 0
    game_points = 0
    for button in butttons:
        button.led.on()
    start_button.led.blink()
    winners_list = []
    winners = SQL('select_all', 'select_winners')
    j = 0
    for winner in winners:
        j += 1
        winners_list.append(
            {
                "num" : j,
                "name": winner[0],
                "rslt": winner[1],
                "foto": "/static/photo/{}".format(winner[2])
            }
        )
    return render_template('history.html', rating = winners_list)

def do_photo(name, path):
    try:
        cap = cv2.VideoCapture(0) # Включаем первую камеру
        for i in range(10): cap.read() # "Прогреваем" камеру, чтобы снимок не был тёмным 
        ret, frame = cap.read() # Делаем снимок 
        #frame = frame[300, 150] обрезать фото
        photo_file = '{}/{}'.format(os.path.join(path, 'static/photo'),name)
        cv2.imwrite(photo_file, frame) # Записываем в файл
        cap.release() # Отключаем камеру
    except:
        return ''
    return ''

def play_music(mp3_file:str):
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()


@app.route('/start')
def start_game():
    global game_phase
    game_phase =1
    for button in butttons:
        button.led.on()
    start_button.led.on()
    gamer_id = SQL('insert','insert_history')
    photo_name = '{}.png'.format(gamer_id)
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    do_photo(photo_name, app.root_path)
    SQL('update', 'update_history',(0, photo_name, gamer_id,))
    return render_template('start.html', foto = '/photo/{}'.format(photo_name))

@app.route('/get_game_phase', methods=['POST'])
def get_game_phase():
    return str(game_phase)

@app.route('/get_game_points', methods=['POST'])
def get_game_points():
    return str(game_points)


def start_button_work():
    global game_phase
    while True:
        time.sleep(0.2)
        if game_phase == 0:
            if start_button.sensor.is_active:
                game_phase = 1
                continue

def but_music_blink(but_num:int):
        play_music('static/music/button.mp3')
        butttons[but_num].led.off()
        time.sleep(3)
        butttons[but_num].led.on()

def buttons_work(): 
    global game_points
    while True:
        time.sleep(0.2)
        if game_phase == 0:
            for i in butttons:
                if i.sensor.is_active:
                    but_action = Thread(target = but_music_blink, args = (i.number,))
                    but_action.start()
                    continue
        else:
            if game_phase ==2:
                sel_but = random.randint(1,len(butttons))
                butttons[sel_but].led.on()
                time_cnt = 0
                while True:
                    if  butttons[sel_but].sensor.is_active:
                        game_points += butttons[sel_but].points_per_click
                    time_cnt += 1
                    time.sleep(0.1)
                    if time_cnt >299:
                        break

if __name__ == '__main__':
    for number in range( len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
    st_work = Thread(target=start_button_work)
    st_work.start()
    ob_work = Thread(target=buttons_work)
    ob_work.start()
    app.run(host='127.0.0.1', port=80, debug=True)
    open_new('127.0.0.1')