import socket
import pickle

HEADERSIZE=10

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

port = 12346

s.bind(('127.0.0.1',port))
print('Socket Binded to',port)
s.listen(1)
print('Waiting For Connection...')

while True:

    clientsocket, address = s.accept()
    print(f'Connection from {address} is established')

    dictionary = {1: "Hello", 2: "This", 3: "Is", 4: "Pickle" }
    msg = pickle.dumps(dictionary)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    print(msg)

    clientsocket.send(msg)

    clientsocket.close()
    print('Connection is closed')
    break
