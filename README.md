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

