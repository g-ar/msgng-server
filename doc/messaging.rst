1 Server
--------

- Server uses sqlite3 to store the messages, so that when the client comes online, it is delivered.

- It also stores the registered users, where the new users are inserted to the database, and deletes when the user unregisters.

- Currently, every message sent is stored with timestamp in the database even if the destination is online. It may be avoided to reduce IO

  - But storing messages may be desired, in cases where multiple devices may be registered for the same user, and all the devices need to be updated when they come online (e.g. Signal)

  - The database is also used to check whether it's duplicate message

2 Client
--------

- First, register if it's new user : r:<username>, which also logs in that registered user

- Sign in if already registered: s:<username>

- Message a destination client by indicating the other user: /<dst>, and then the subsequent messages typed will go to that <dst>

- The user <dst> gets the message if online, otherwise it receives that message after coming online

- <dst> can reply back by first typing /<src>, and then the messages typed will go to that <src>

3 Sequence Diagram
------------------

- Some of the possible actions are shown below:

.. code-block:: text

    +---------+          +---------+            +---------+    
    |         |          |         |            |         |    
    | Client1 |          | Server  |            | Client2 |    
    +----+----+          +----+----+            +----+----+    
         |                    |                      |         
         | ["register","c1"]  |                      |         
         |------------------->|                      |         
         | ["info",           |                      |
         |  "registered"]     |                      |
         |<-------------------|  ["signin","c2"]     |         
         |                    |<---------------------|         
         |                    |  ["info",            |
         |                    |    "signed in"]      |
         |                    |--------------------->|         
         |["send", "c2",      |                      |         
         | "hello"]           |                      |         
         |------------------->|                      |         
         |                    |[timestamp, "c1"      |         
         |                    |            "hello"]  |         
         |                    |--------------------->|         
         |                    |["send", "c1", "hi"]  |         
         |                    |<---------------------|         
         |[timestamp, "c2",   |                      |         
         |            "hi"]   |                      |         
         |<-------------------|                      |         
         |                    |                      |         
         | ["signout"]        |                      |         
         |------------------->|                      |         
         | ["signed out"]     |                      |         
         |<-------------------|                      |         
         |                    | ["unregister"]       |         
         |                    |<---------------------|         
         |                    | ["unregistered"]     |         
         |                    |--------------------->|         
         o                    o                      o         

4 Message Format
----------------

To reduce the message overhead, a simple header and data format is used, instead of larger xml or json structures. 
The requests and responses are outlined below:

- Register

  .. code-block:: js
      

      ["register", "username"]
      ["info", "Registered and signed in"]

- Signin

  .. code-block:: js
      

      ["signin", "username"]
      ["info", "Signed in"]

- Send messages

  .. code-block:: js
      

      ["send", "destination", "the message"]  

  - If client is offline

    .. code-block:: js
        

        ["info", "<dst> offline"]

  - If <dst> does not exist

    .. code-block:: js
        

        ["info", "<dst> unregistered"]

  - When <dst> comes online, it receives:

    .. code-block:: js
        

        ["msg", "<src>", timestamp, "the message"]

  - If duplicate msg is sent, <src> receives

    .. code-block:: js
        

        ["info", "duplicate msg: dropped"]

- Signout
  Close the connection to client and remove from the "active" list in the server

  .. code-block:: js
      

      ["signout"]

- Unregister
  Close the connection and remove from the user database

  .. code-block:: js
      

      ["unregister"]

5 TODO 
-------

- Add encryption

- Add authentication

- Use in-memory database for reducing IO latency, like redis

- Profile the server and quantify results to suggest optimizations

- Including header, the message length is fixed to 1024 chars, and limited to only text messages
