import sqlite3
import json
from .constants import DATABASE

def create_db():
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL UNIQUE)")
    c.execute("CREATE TABLE IF NOT EXISTS messages (src TEXT NOT NULL, dst TEXT NOT NULL, msg TEXT NOT NULL, ts INTEGER NOT NULL, recd INTEGER NOT NULL)")
    con.commit()
    con.close()

def add_to_users(name):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        c.execute("INSERT INTO users VALUES (?)",(name, ))
        con.commit()
        val = True
    except Exception as e:
        print e
    con.close()
    return val

def del_from_users(name):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        c.execute("DELETE FROM users WHERE name = ?",(name, ))
        con.commit()
        val = True
    except Exception as e:
        print e
    con.close()
    return val

def check_users(name):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        lst = c.execute("SELECT * FROM users WHERE name = ?",(name, )).fetchall()
        if len(lst) == 1:
            val = True
        con.commit()
    except Exception as e:
        print e
    con.close()
    return val

def send_undelivered_messages(name, users):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        lst = c.execute("SELECT src, msg, ts FROM messages WHERE dst = ? AND recd = 0",(name, )).fetchall()
        conn = users[name]
        for l in lst:
            sndmsg = ["msg", l[0], l[2], l[1]]
            conn.send(json.dumps(sndmsg)+"\n")
        c.execute("UPDATE messages SET recd = 1 WHERE dst = ? AND recd = 0",(name, ))
        con.commit()
    except Exception as e:
        print e
    con.close()
    return val

def is_dup(src, dst, msg, ts):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        lst = c.execute("SELECT * FROM messages WHERE src = ? and dst= ? and msg = ? and ?-ts < 5",(src, dst, msg, ts)).fetchall()
        if len(lst) > 0:
            val = True
        con.commit()
    except Exception as e:
        print e
    con.close()
    return val

def add_to_messages(src, dst, msg, ts, recd):
    con = sqlite3.connect(DATABASE['path'])
    c = con.cursor()
    val = False
    try:
        c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?)",(src, dst, msg, ts, recd))
        con.commit()
    except Exception as e:
        print e
    con.close()
    return val
