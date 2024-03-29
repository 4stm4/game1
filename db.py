import sqlite3, datetime, pysnooper
from config import file_db

cnn = sqlite3.connect(file_db, check_same_thread=False, isolation_level = None)
queries = {
'select_winners' : "SELECT name, result, photo  FROM history ORDER BY result DESC LIMIT 5",
'insert_history' : "INSERT INTO history (name, 'result', photo) VALUES ('', 0, '')",
'update_history' : "UPDATE history SET  photo= '%s' WHERE id= %s",
'update_points'  : "UPDATE history SET 'result'= %s WHERE id= %s"
}

def SQL(action:str, query_name:str, *args):
    if args:
        query = queries[query_name] % args[0]
    else:
        query = queries[query_name]
    try:
        cur = cnn.cursor()
        res = cur.execute(query)
    except:
        return 'DB ERROR'
    if action == 'select_one':
        res = cur.fetchone()
    if action == 'select_all':
        res = cur.fetchall()
    if action in ('insert'):
        cnn.commit()
        return cur.lastrowid
    if action in ('update'):
        cnn.commit()
    return res