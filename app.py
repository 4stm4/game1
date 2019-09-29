import datetime, json, sqlite3, pysnooper
from flask import Flask, render_template
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_pyfile('config.ini')
cnn = sqlite3.connect(app.config['DBASE'], check_same_thread=False, isolation_level = None)
scheduler = APScheduler()
scheduler.start()
view_history   = "SELECT name, result, photo  FROM history ORDER BY result DESC LIMIT 5"
insert_history = "INSERT INTO history (name, 'result', photo) VALUES (?,?,?)"



def ins_game_hist(id, status, uptime):
    cur = cnn.cursor()
    res = cur.execute(insert_history, (id, status, uptime, datetime.datetime.now(),))
    cnn.commit()

#@scheduler.task('interval', id='main_circle', seconds=5)
def main_circle():
    pass

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
    return render_template('history.html', rating = history_list)

@app.route('/start')
def game():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)