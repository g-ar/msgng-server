## About

A Simple Messaging Server which waits for client connections, and allows clients to message each other.

## Run

Requires python2.7

- Run server
```
$ python server.py
```
  
- Run clients in different hosts or terminals. More details can be found in doc.
```
$ python client.py
Signin or register
r:A -- to register user A, s:A -- to signin user A
s:b
signed in
/a
Hi
a> 1482552502 Hello
#
```
```
$ python client.py
Signin or register
r:A -- to register user A, s:A -- to signin user A
s:a
signed in
b> 1482552496 Hi
/b
Hello
#
```

- Telnet can also be used as a client to send raw commands
```
$ telnet localhost 6666
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
["info", "Signin or register"]
["register", "name1"]
["info", "registered and signed in"]
["send", "name2", "Hello"]
["info", "name2 unregistered"]
["signout"]
["info", "signed out"]
Connection closed by foreign host.
```