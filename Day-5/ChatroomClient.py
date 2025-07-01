import socket
import errno
import sys

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 12347

my_user = input("Username: ")

c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c_socket.connect((IP, PORT))

c_socket.setblocking(False)

user = my_user.encode('utf-8')
user_header = f"{len(user):<{HEADER_LENGTH}}".encode('utf-8')

c_socket.send(user_header + user)

while True:
    message = input(f"{my_user} -> ")

    # Use 'CLOSE CONNECTION' to end connection with server
    if message == 'CLOSE CONNECTION':
        print('Connection closed with server')
        c_socket.close()    
        sys.exit()

    else:

        if len(message) > 0:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            c_socket.send(message_header + message)

        try:
            while True:
                user_header = c_socket.recv(HEADER_LENGTH)

                if len(user_header) <=0:
                    print('Connection closed with server')
                    sys.exit()

                user_length = int(user_header.decode('utf-8'))
                user = c_socket.recv(user_length).decode('utf-8')    

                message_header = c_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8'))
                message = c_socket.recv(message_length).decode('utf-8')

                print(f"{user} -> {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading Error: {}'.format(str(e)))
                sys.exit()

            continue

        except Exception as e:
            print('Reading Error: {}'.format(str(e)))
            sys.exit()

