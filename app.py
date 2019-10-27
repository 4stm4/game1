import datetime, json, sqlite3, cv2, time, os, pysnooper
from flask import Flask, render_template, send_from_directory
from pygame import mixer
from threading import Thread
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
cnn = sqlite3.connect(app.config['DBASE'], check_same_thread=False, isolation_level = None)
scheduler = APScheduler()
scheduler.start()
cnt = 0
view_history   = "SELECT name, result, photo  FROM history ORDER BY result DESC LIMIT 5"
insert_history = "INSERT INTO history (name, 'result', photo) VALUES (?,?,?)"


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

def ins_game_hist(id, status, uptime):
    cur = cnn.cursor()
    res = cur.execute(insert_history, (id, status, uptime, datetime.datetime.now(),))
    cnn.commit()

@app.route('/')
@pysnooper.snoop()
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
    return render_template('history.html', rating = history_list)

@app.route('/start')
@pysnooper.snoop()
def game():
    #m = Thread(target = do_photo, args = ('00051.jpeg',))
    #m.start()
    do_photo('00051.jpeg')
    t = Thread(target=play_music, args = ('static/music/start_game.mp3',))
    t.start()
    return render_template('start.html', foto = '/photo/00051.jpeg')
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)