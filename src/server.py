import socket
import thread
import time
import json
from helpers.dblib import *
from helpers.constants import *


def accept(conn):
    def threaded():
        while True:
            try:
                conn.send('''["info", "Signin or register"]\n''')
            except socket.error:
                break                     # break if user terminates without reg/signin
            
            try:
                msg = conn.recv(1024).strip()
                msg = json.loads(msg)     # just a list, number of elements depend on the command
                cmd = msg[0]
                name = msg[1]
                try:
                    if cmd == "register": # Once the name is register, remain here till signin cmd is received
                        res = add_to_users(name)
                        if res:
                            conn.send('''["info", "registered and signed in"]\n''')
                            conn.setblocking(False)
                            users[name] = conn
                            break
                        else:
                            conn.send('''["info", "registration failed"]\n''')
                            continue
                    elif cmd == "signin":
                        if check_users(name):
                            conn.send('''["info", "signed in"]\n''')
                            conn.setblocking(False)
                            users[name] = conn
                            send_undelivered_messages(name, users)
                            break                                       # Go out of here to message other clients
                        else:
                            conn.send('''["info", "ID not found"]\n''') # remain till registered and signed in
                    else:
                        conn.send('''["info", "signin to chat"]\n''')
                        continue
                except Exception:
                    conn.send('''["info", "Malformed message"]\n''') 
            except socket.error:
                continue
            except ValueError:
                continue
    thread.start_new_thread(threaded, ())


def unicast(src, dst, msg):
    try:
        ts = int(time.time())
        if dst in users:
            conn = users[dst]
            if not is_dup(src, dst, msg, ts):
                add_to_messages(src, dst, msg, ts, 1)
                sndmsg = ["msg", src, ts, msg]
            else:
                sndmsg = ["info", "duplicate msg: dropped"]
                conn = users[src]
        else:
            conn = users[src]
            if check_users(dst):
                if not is_dup(src, dst, msg, ts):
                    add_to_messages(src, dst, msg, ts, 0)
                sndmsg = ["info", dst+" offline"]
            else:
                sndmsg = ["info", dst+" unregistered"]
        conn.send(json.dumps(sndmsg)+"\n")
    except socket.error:
        pass


if __name__ == "__main__":
    # Set up the server socket.
    users = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind((HOST, PORT))
    server.listen(1)
    print "Listening on %s" % ("%s:%s" % server.getsockname())
    
    create_db()
    
    while True:
        try:
            # Accept new connections.
            while True:
                try:
                    conn, addr = server.accept()
                except socket.error:
                    break
                accept(conn)
            # Read from connections.
            for name, conn in users.items():
                try:
                    msg = conn.recv(1024)
                except socket.error:
                    continue
                if not msg:
                    # Disconnect on empty string 
                    del users[name]
                else:
                    msg = json.loads(msg)
                    cmd = msg[0]
                    if cmd == "signout":
                        del users[name]
                        sndmsg = ["info", "signed out"]
                        conn.send(json.dumps(sndmsg)+"\n")
                    elif cmd == "unregister":
                        del users[name]
                        del_from_users(name)
                        sndmsg = ["info", "unregistered"]
                        conn.send(json.dumps(sndmsg)+"\n")
                    elif cmd == "send":
                        unicast(name, msg[1], msg[2])                        
                    else:
                        sndmsg = ["info", "unknown cmd"]
                        conn.send(json.dumps(sndmsg)+"\n")
            time.sleep(.1)
        except (SystemExit, KeyboardInterrupt):
            break
        except ValueError:
            continue
