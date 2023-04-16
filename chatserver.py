# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: jcarte39
# Member 2: mmaka4
# Member 3: mkhala6


# Note: 
# This starter code is optional. Feel free to develop your own solution. 

# Import any necessary libraries below
import socket
import threading
import sys, os, struct

# Any global variables
BUFFER = 4096
print_lock = threading.Lock()
file = "credentials.txt"
list_of_clients = []

"""
The thread target fuction to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def threaded(c):

    while True:

        data = c.recv(BUFFER).decode('utf-8')

        if not data:
            print_lock.release()
            break

    c.close()


def chatroom (c):
    # Task1: login/register the user
    print('Chatroom starting')
    username = c.recv(BUFFER).decode('utf-8')
    print(f"received username: {username}")

    password = ""

    if not (os.path.exists("credentials.txt")):
        print("File does not exist, creating new file...")
        infile = open(file, 'x', encoding='utf-8')
        infile.close()
    else:
        print("File exists, reading file...")
        infile = open(file, 'r', encoding='utf-8')

    user_answer = ""
    pass_answer = ""

    for line in infile:
        if username in line:
            user_answer = "Existing user"
            c.send(user_answer.encode('utf-8'))
            correct = False

            while correct == False:
                password = c.recv(BUFFER)
                password = password.decode('utf-8')
                if password in line:
                    pass_answer = "Login successful"
                    c.send(pass_answer.encode('utf-8'))
                    correct = True
                else:
                    pass_answer = "Incorrect password"
                    c.send(pass_answer.encode('utf-8'))
            infile.close()
        else:
            user_answer = "Creating new user."
            c.send(user_answer.encode('utf-8'))

            pass_answer = "Enter new password: "
            c.send(pass_answer.encode('utf-8'))

            password = c.recv(BUFFER)
            password = password.decode('utf-8')

            outfile = open(file, 'a', encoding='utf-8')
            print(f'{username}, {password}', file=outfile)
            outfile.close()

    list_of_clients.append((c, username))
   

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:

        # assigning username to client for messaging purposes
        for client in list_of_clients:
            if client[0] == c:
                senders_username = client[1]

        c.send("Enter BM for broadcast message, PM for private message, or EX to exit chatroom: ")
        data = c.recv(BUFFER).decode('utf-8')

        if not data:
            break

        if data == "BM":
            c.send("Broadcast message. Enter message: ")
            broadcast_message(c.recv(BUFFER), c, senders_username)
            c.send("Message sent.")


        elif data == "PM":
            message = "Users in chatroom: \n"
            for client in list_of_clients:
                message += client[1] + "\n"

            c.send(message)

            c.send("Private message. Enter recipient's username: ")

            while True:
                recipients_username = c.recv(BUFFER).decode('utf-8')

                if recipients_username not in message:
                    c.send("N")
                else:
                    c.send("Y")
                    break

            c.send("Enter message: ")
            private_message(c.recv(BUFFER), recipients_username, senders_username)
            c.send("Message sent.")


        elif data == "EX":
            c.send("Exiting chatroom...")
            list_of_clients.remove((c, username))

            """for client in list_of_clients:
                if client[0] == c:
                    list_of_clients.remove(client)
            break"""



def broadcast_message(message, senders_conn, senders_username):
    for client in list_of_clients:
        if client[0] != senders_conn:
            client.send(f"**BM** {senders_username}: {message}")




def private_message(message, recipients_username, senders_username):
    for client in list_of_clients:
        if client[1] == recipients_username:
            client[0].send(f"**PM** {senders_username}: {message}")


def main(port):
     # TODO: Validate input arguments
    HOST = '192.168.56.1'
    PORT = int(port)
    sin = (HOST, PORT)

    # TODO: create a socket in UDP or TCP
    try:
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()
    
    # TODO: Bind the socket to address
    try:
        opt = 1
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt)
        serversock.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    serversock.listen(5) # 5 is the number of connections that can be queued
    print("Socket is listening...")

    while True:
        print(f"Waiting for connections on port {PORT}")

        # TODO: handle any incoming connection with UDP or TCP
        conn, addr = serversock.accept()

        # TODO: initiate a thread for the connected user
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        
        threading.Thread(target=threaded,
            args=(conn,),
        ).start()
        
        chatroom(conn)

    s.close()
        
       

if __name__ == '__main__':
    main(sys.argv[1])
