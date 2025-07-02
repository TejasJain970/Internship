import socket
import time

HEADER_LENGTH = 10

IP = '127.0.0.1'
PORT = 12348

c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

c_socket.connect((IP, PORT))
print('\nSuccessfully connected to server')

print('\nThe Equation : (2*i) + (i/2) + ((i*i)/10000)\n')

while True:
        try:
            int_i = int(input('Give starting value of i (Maximum 10000) :'))
            if int_i > 10000 or int_i <= 0:
                print('Please enter valid integer ranging from 1 to 10000\n')
                continue
            break

        except:
            print('Please enter valid integer ranging from 1 to 10000\n')
            continue
    
string_i = str(int_i)        
total_iterations = 10000 - int_i + 1

start = time.perf_counter()

for int_i in range(total_iterations):
    sum = ((2*int_i) + (int_i/2) + ((int_i*int_i)/10000))
    int_i = int_i + 1 
    print(f'{sum}')
    time.sleep(0.002)
    result_message = str(sum)
    message = result_message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    c_socket.send(message_header + message)

finish = time.perf_counter()

string_time = str(round(finish-start, 5))
message_time = (f"\nFinished in {string_time} seconds(s)")
final_time = message_time.encode('utf-8')
final_time_header = f"{len(final_time):<{HEADER_LENGTH}}".encode('utf-8')
c_socket.send(final_time_header + final_time)

message_input = (f'\nStarting value of i :{string_i} and Total no. of iterations :{total_iterations}')
input = message_input.encode('utf-8')
input_header = f"{len(input):<{HEADER_LENGTH}}".encode('utf-8')

c_socket.send(input_header + input)

print(f'\nFinished in {round(finish-start, 5)} seconds(s)')
