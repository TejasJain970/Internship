import socket
import sys

HEADER_LENGTH = 10

IP = '127.0.0.1'
PORT = 12348

print('\nThe Equation : (2*i) + (i/2) + ((i*i)/10000)\n')
s_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s_list = [s_socket]
clients = {}
has_run_once = False

s_socket.bind((IP, PORT))
s_socket.listen()
print(f'Listening for connection on {IP} : {PORT}.....\n')

def receive(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if len(message_header) <= 0:
            return False 

        message_length = int(message_header.decode('utf-8'))
        return{'header': message_header, 'data': client_socket.recv(message_length)}    
    
    except Exception:
        return False
    
c_socket, c_address = s_socket.accept()
print('Accepted new connection from {}:{}\n'.format(*c_address))

while True:  
    
    while True:
        message = receive(c_socket)
        
        if message is False:
            print('\nClosed connection with client')
            sys.exit()
        
        else:
            print(f'{message["data"].decode("utf-8")}')    

    


  



