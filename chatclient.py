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
from _thread import *
import threading
import sys, os, struct
import time

# Any global variables
BUFFER =  4096




"""
The thread target fuction to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""
def accept_messages(clientsock):
    while True:
        message = clientsock.recv(BUFFER).decode('utf-8')
        message_split = [char for char in message]
        if message_split[0] == '*':
            print(f'\n{message}')
            print("Please enter a command: ")


def main(host, port, username):
     # TODO: Validate input arguments
    HOST = host
    PORT = int(port)
    sin = (HOST, PORT)



    # TODO: create a socket with UDP or TCP, and connect to the server
    try:
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()
    
    # TODO: connect to server
    try:
        print(f"Attempting to connect to the server: {sin}")
        clientsock.connect(sin)
        print("Connection established.")
    except socket.error as e:
        print("Failed to connect to the server.")
        sys.exit()
    
    clientsock.send(username.encode('utf-8'))
    user_answer = clientsock.recv(BUFFER).decode('utf-8')
    print(user_answer)

    while True:

        pass_answer = ""
        pass_answer = clientsock.recv(BUFFER).decode('utf-8')
        
        while pass_answer == "Incorrect password" or pass_answer == "" or pass_answer == "Enter new password: ":
            if pass_answer == "Enter new password: ":
                message = input("Please enter a new password: ")
                message_bytes = message.encode('utf-8')
                try:
                    clientsock.send(message_bytes)
                except socket.error as e:
                    print('Failed to send message.')
                    sys.exit()
                break
            else:
                message = input("Please enter your password: ")
                message_bytes = message.encode('utf-8')
                try:
                    clientsock.send(message_bytes)
                except socket.error as e:
                    print('Failed to send message.')
                    sys.exit()
                pass_answer = clientsock.recv(BUFFER).decode('utf-8')
                print(pass_answer)
        else:
            break

    # TODO: initiate a thread for receiving message
    message_thread = threading.Thread(target=accept_messages, args=(clientsock, ))
    message_thread.start()

    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        count = 0
        if count == 0:
            message = input("Please enter a command: ")
            clientsock.send(message.encode('utf-8'))
            count += 1
        else:
            message = input()
            clientsock.send(message.encode('utf-8'))

        # EX
        if message == 'EX':
            print('Connection closed.')
            clientsock.close()
            break

        # BM
        if message == 'BM':
            print(clientsock.recv(BUFFER).decode('utf-8'))
            clientsock.send(input('> ').encode('utf-8'))
            print(clientsock.recv(BUFFER).decode('utf-8'))
            continue

        elif message == 'PM':
            # user list
            print(clientsock.recv(BUFFER).decode('utf-8'))

            # username prompt
            ack = "N"
            while ack == "N":
                print("Please enter an online member's username:")
                clientsock.send(input('> ').encode('utf-8'))
                ack = clientsock.recv(BUFFER).decode('utf-8')

            clientsock.send(input(f"{clientsock.recv(BUFFER).decode('utf-8')} ").encode('utf-8'))
            print(clientsock.recv(BUFFER).decode('utf-8'))
            continue


if __name__ == '__main__': 
    main(sys.argv[1], sys.argv[2], sys.argv[3])