import socket

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

    msg = "Thou shall never forget network connection between Server and Client using Socket"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg

    clientsocket.send(bytes(msg,"utf-8"))

    clientsocket.close()
    print('Connection is closed')
    break
