README - PYTHON 3.10
------------

chatserver.py

Runs a multithreaded server for clients to connect to, login, and chat on.

Use the following command to start the program:

python3 chatserver.py <port>



Accepts following commands from client users:

BM - Broadcast message to all users

PM <user> - Privately messages an online user

EX - Exits the chatroom



Accesses a credentials file during operation, and will create it if it does not exist already.

-------------

chatclient.py

Runs a client that can connect to a chat server after logging in or creating a new user.

Use the following command to start the program:

python3 chatclient.py <hostname> <port> <username>



Utilizes the following commands:

BM - Broadcast message to all users

PM <user> - Privately messages an online user

EX - Exits the chatroom

------------

credentials.txt

The text file used to store usernames and passwords.

