import socket             

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
print ("Socket Created")

port = 12345                

s.bind(('127.0.0.1', port))         
print ("socket binded to %s" %port) 

s.listen(1)     
print ("socket is listening")            

while True: 

  c, addr = s.accept()     
  print ('Got connection from', addr )

  c.send('Server Successfully Connected to Client'.encode()) 
  c.close()
  break