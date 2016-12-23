import socket
import threading
import time
import json

HOST = "localhost"
PORT = 6666

client = socket.create_connection((HOST, PORT))
data = json.loads(client.recv(1024))
if data[0] == "info":
    print data[1]
ip = raw_input('r:A -- to register user A, s:A -- to signin user A\n')
cmd, user = ip.split(':')
if cmd == "r":
    client.send(json.dumps(["register", user]))
if cmd == "s":
    client.send(json.dumps(["signin", user]))
data = client.recv(1024)
data = json.loads(data)
if data[0] == "info":
    print data[1]

finished = False
def resp():
    while True:
        data = client.recv(1024).split('\n')
        try:
            for d in data:
                msg = json.loads(d)
                if msg[0] == "info":
                    print msg[1]
                if msg[0] == "msg":
                    print msg[1]+">", msg[2], msg[3]
        except ValueError:
            pass
        
th = threading.Thread(target=resp)
th.setDaemon(True)
th.start()

while not finished:
    ip = raw_input()
    try:
        if ip[0] == "/":
            frnd = ip[1:]
            continue
        elif ip[0] == "#":
            sndmsg = ["signout"]
            finished = True
        elif ip[0] == "!":
            sndmsg = ["unregister"]
            finished = True
        else:
            sndmsg = ["send", frnd, ip]
        client.send(json.dumps(sndmsg))
    except IndexError:
        pass

client.close()