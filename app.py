""" Игра для батутной арены"""
import pysnooper
import time
import os
import random
from threading import Thread
import cv2
from pygame import mixer
from flask import Flask, render_template, send_from_directory
from db import SQL
from buttons import butttons, start_button, buttons_specs, BUTTON
from config import led_delay, game_time, result_time, start_sound, end_sound, press_sound, press_delay

APP = Flask(__name__)
APP.config.from_pyfile('config.ini')
GAME_PHASE = 0  # 0 - ожидание, 1 - старт, 2 игра, 3 - результаты
ACTIVE_BUTTON = -1
GAME_POINTS = 0
GAMER_ID = -1
GAME10 = False
#camera = cv2.VideoCapture(0) # Включаем первую камеру

@APP.route('/photo/<filename>')
def photo(filename):
    """Метод выдаёт фотографии из рейтинга
    """
    return send_from_directory(os.path.join(APP.root_path, 'static/photo'), filename,
                               mimetype='image')

@APP.route('/music/<filename>')
def music(filename):
    """ Метод передаёт файлы звуков
    """
    return send_from_directory(os.path.join(APP.root_path, 'static/music'), filename,
                               mimetype='audio')

@APP.route('/game')
def game():
    """Фаза игры
    """
    global GAME_PHASE, GAME_POINTS
    GAME_PHASE = 2
    for button in butttons:
        button.led.off()
    start_button.led.off()
    return render_template('game.html', foto='/photo/{}.png'.format(GAMER_ID))

@APP.route('/game_over')
def game_over():
    """Фаза завершения игры
    """
    global GAME_PHASE, GAME_POINTS, GAMER_ID
    GAME_PHASE = 3
    SQL('update', 'update_points', (GAME_POINTS, GAMER_ID,))
    for button in butttons:
        button.led.on()
    start_button.led.on()
    return render_template('game_over.html', points=GAME_POINTS,
                           foto='/photo/{}.png'.format(GAMER_ID))

@APP.route('/')
def index():
    """Фаза ожидания начала игры
    """
    global GAME_PHASE, GAME_POINTS, GAMER_ID
    GAME_PHASE = 0
    GAME_POINTS = 0
    GAMER_ID = -1
    for button in butttons:
        button.led.off()
    start_button.led.on()
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
    return render_template('history.html', rating=winners_list)

def do_photo(name, path):
    """Метод делает фотографию
    """
    global camera
    try:
        camera = cv2.VideoCapture(0) # Включаем первую камеру
        camera.read() # "Прогреваем" камеру, чтобы снимок не был тёмным
        time.sleep(0.5)
        ret, frame = camera.read() # Делаем снимок
        #frame = frame[300, 150] обрезать фото
        #cv2.ROTATE_90_CLOCKWISE
        #cv2.ROTATE_90_COUNTERCLOCKWISE
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        photo_file = '{}/{}'.format(os.path.join(path, 'static/photo'), name)
        cv2.imwrite(photo_file, frame) # Записываем в файл
        camera.release() # Отключаем камеру
    except Exception as err:
        return 'ERROR = {}'.format(err)
    return ''

def play_music(mp3_file: str):
    """Метод проигрывает звуки
    """
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()

@APP.route('/start')
def start_game():
    """Фаза начала игры
    """
    global GAME_PHASE, GAMER_ID#, camera
    #camera.release() # Отключаем камеру
    if GAME_PHASE == 1:
        GAME_PHASE = 2
        GAME10 = False
        for button in butttons:
            button.led.on()
        start_button.led.on()
        GAMER_ID = SQL('insert', 'insert_history')
        photo_name = '{}.png'.format(GAMER_ID)
        do_photo(photo_name, APP.root_path)
        thread_music = Thread(target=play_music, args = (start_sound,))
        thread_music.start()

        SQL('update', 'update_history',( photo_name, GAMER_ID,))
    return render_template('start.html', foto = '/photo/{}.png'.format(GAMER_ID))

@APP.route('/get_game_phase', methods=['POST'])
def get_game_phase():
    """Метод выдаёт фазу игры
    """
    global GAME_PHASE
    return str(GAME_PHASE)

@APP.route('/get_game_points', methods=['POST'])
def get_game_points():
    """Метод возвращает количество игровых очков
    """
    global GAME_POINTS
    return str(GAME_POINTS)

def start_button_work():
    """Метод работы стартовой кнопки
    """
    global GAME_PHASE
    while True:
        time.sleep(0.2)
        if GAME_PHASE == 0:
            if start_button.sensor.is_active:
                play_music('static/music/button.mp3')
                GAME_PHASE = 1
                continue

def buttons_work(): 
    """Метод работы игровых кнопок
    """
    global GAME_POINTS, GAME_PHASE, GAME10
    start_button_num = len(butttons)
    last_two = [0,1]
    while True:
        time.sleep(0.04)
        if GAME_PHASE == 0:
            for i in butttons:
                if i.sensor.is_active:
                    play_music(press_sound)
                    butttons[i.number].led.on()
                    time.sleep(led_delay)
                    butttons[i.number].led.off()
                    continue
        else:
            if GAME_PHASE == 2:
                sel_but = -1
                while True:
                    sel_but = random.randint(0,len(butttons))
                    if not sel_but in last_two:
                        break
                last_two.append(sel_but)
                last_two.pop(0)
                if sel_but == start_button_num:
                    start_button.led.on()
                else:
                    butttons[sel_but].led.on()
                time_cnt = 0
                sign_cnt = 0
                while True:
                    if sel_but == start_button_num:
                        if start_button.sensor.is_active:
                            sign_cnt += 1
                            if sign_cnt > 3:
                                if not GAME10:
                                    music_button = Thread(target = play_music, args = ('static/music/button.mp3',))
                                    music_button.start()
                                GAME_POINTS += start_button.points_per_click
                                start_button.led.off()
                                break
                            time.sleep(0.05)
                            continue
                    else:
                        if  butttons[sel_but].sensor.is_active:
                            sign_cnt += 1
                            if sign_cnt > 3:
                                if not GAME10:
                                    music_button = Thread(target = play_music, args = ('static/music/button.mp3',))
                                    music_button.start()
                                GAME_POINTS += butttons[sel_but].points_per_click
                                butttons[sel_but].led.off()
                                break
                            time.sleep(0.05)
                            continue
                    sign_cnt = 0
                    time_cnt += 1
                    time.sleep(0.1)
                    if time_cnt >29:
                        if sel_but == start_button_num:
                            start_button.led.off()
                        else:
                            butttons[sel_but].led.off()
                        break

@APP.route('/end_music', methods=['POST'])
def end_music():
    """Метод проигрывает музыку об окончании игры
    """
    global GAME10
    GAME10 = True
    thread_music2 = Thread(target=play_music, args = (end_sound,))
    thread_music2.start()
    return ''

if __name__ == '__main__':
    for number in range(len(buttons_specs)):
        butttons.append(BUTTON(number, *buttons_specs[number]))
    st_work = Thread(target=start_button_work)
    st_work.start()
    ob_work = Thread(target=buttons_work)
    ob_work.start()
    APP.run(host='127.0.0.1', port=8080)
