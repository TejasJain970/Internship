import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12347

s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s_socket.bind((IP, PORT))
s_socket.listen()
print(f'Listening for connection on {IP} : {PORT}.....')

s_list = [s_socket]
clients = {}

def receive(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if len(message_header) <= 0:
            return False 

        message_length = int(message_header.decode('utf-8'))
        return{'header': message_header, 'data': client_socket.recv(message_length)}    
    
    except Exception:
        return False
    
while True:
    read_sockets, _, exception_sockets = select.select(s_list, [], s_list) 
        
    for notified_sockets in read_sockets:
        if notified_sockets == s_socket:
            c_socket, c_address = s_socket.accept()

            user = receive(c_socket)    
            if user is False:
                continue

            s_list.append(c_socket)

            clients[c_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*c_address, user['data'].decode('utf-8')))

        else:
            message = receive(notified_sockets)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_sockets]['data'].decode('utf-8')))
                s_list.remove(notified_sockets)
                del clients[notified_sockets]
                continue

            user = clients[notified_sockets]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for c_socket in clients:
                if c_socket != notified_sockets:
                    c_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


    for notified_sockets in exception_sockets:
        s_list.remove(notified_sockets)
        del clients[notified_sockets]



