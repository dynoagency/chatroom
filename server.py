import socket
import threading
import os
import time
import datetime as dt
from colored import fg,attr,bg


connected = fg("green")
disconnected = fg("red")
cyan = fg("cyan")
reset = attr("reset")

# Connection Data
os.system('cls')
host = input(cyan + "(for localhost, 127.0.0.1)\nHost--> " + reset)
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

def console():
    while True:
        input("# ")

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            print(disconnected + "{} left".format(nickname)+reset)
            file = open(f"chatlogs.txt", "a") 
            file.write(f"[{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {nickname} left the chat \r")
            file.close()
            print("")
            nicknames.remove(nickname)
            break
# Receiving / Listening Function89458 
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(cyan + "Connected with {}".format(str(address)) + reset)

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(cyan+"Nickname is {}".format(nickname)+reset)
        file = open(f"chatlogs.txt", "a") 
        file.write(f"[{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connected with {address}, nick is {nickname} \r")
        file.close()
        print("")
        client.send("----------#".encode('ascii'))
        client.send('Connected to server!\n'.encode('ascii'))
        client.send("Welcome {}, enjoy the __ shit tcp chatroom\nand be a good guy!\n".format(nickname).encode('ascii'))
        client.send("----------\n".encode('ascii'))

        broadcast("{} joined!\n".format(nickname).encode('ascii'))
        
        
        

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


os.system('cls')
print(connected + "Server is started..." + reset)
print("")
receive()
