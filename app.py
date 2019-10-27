import datetime, sqlite3, cv2, time, os, pysnooper
import RPi.GPIO as GPIO
from flask import Flask, render_template, send_from_directory
from pygame import mixer
from threading import Thread

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
cnn = sqlite3.connect(app.config['DBASE'], check_same_thread=False, isolation_level = None)
view_history   = "SELECT name, result, photo  FROM history ORDER BY result DESC LIMIT 5"
insert_history = "INSERT INTO history (name, 'result', photo, dt) VALUES (' ', 0, '', ?)"
update_history = "UPDATE history SET 'result'= {}, photo= '{}' WHERE id= {}"
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/photo'),filename, mimetype='image')

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'),filename, mimetype='audio')

def do_photo(name):
    cap = cv2.VideoCapture(0) # Включаем первую камеру
    for i in range(30): cap.read() # "Прогреваем" камеру, чтобы снимок не был тёмным 
    ret, frame = cap.read() # Делаем снимок 
    #frame = frame[300, 150] обрезать фото
    photo_file = '{}/{}'.format(os.path.join(app.root_path, 'static/photo'),name)
    cv2.imwrite(photo_file, frame) # Записываем в файл
    cap.release() # Отключаем камеру
    return ''

def play_music(mp3_file:str):
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()

def ins_game_hist():
    cur = cnn.cursor()
    res = cur.execute(insert_history, (datetime.datetime.now(),))
    cnn.commit()
    return cur.lastrowid

def upd_game_hist(result,photo,gamer_id):
    cur = cnn.cursor()
    query =update_history.format(result, photo, gamer_id)
    print(query)
    res = cur.execute(query)
    cnn.commit()

@app.route('/')
def index():
    history_list = []
    cur = cnn.cursor()
    cur.execute(view_history)
    res = cur.fetchall()
    j = 0
    for i in res:
        j += 1
        history_list.append(
            {
                "num" : j,
                "name": i[0],
                "rslt": i[1],
                "foto": "/static/photo/{}".format(i[2])
            }
        )
        z = Thread(target = wait_start_button())
        z.start()
    return render_template('history.html', rating = history_list)

def wait_start_button():
    while GPIO.input(10) == GPIO.LOW:
        time.sleep(0.01) 
    print('button pressed')
    game()

@app.route('/start')
def game():
    gamer_id = ins_game_hist()
    photo_name = '{}.jpeg'.format(gamer_id)
    do_photo(photo_name)
    upd_game_hist(0, photo_name, gamer_id)
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    return render_template('start.html', foto = '/photo/{}'.format(photo_name))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)