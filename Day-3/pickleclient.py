import socket
import pickle

HEADERSIZE = 10

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

port = 12346

s.connect(('127.0.0.1',port))

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)

        if len(msg) <= 0:
            break

        if new_msg:
            print(f"New Message Lenght: {msg[:HEADERSIZE]}")
            msglength = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"Full Message Lenght: {msglength}")

        full_msg = full_msg + msg
        print("Lenght of Decoded Message:",len(full_msg))

        if len(full_msg) - HEADERSIZE == msglength:
            print(f"Full Message Received: {full_msg[HEADERSIZE:]}")
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True        

    if len(msg) <= 0:
        break       
        