import socket
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host=socket.gethostname()
port=5000
s.bind((host,port))
s.listen(1)
# print(host)
# print("waiting for connection")
conn, addr= s.accept()
# print(addr, "has connected!")
filename=input(str("enter filename"))
file=open(filename,'rb')
file_data=file.read(1024)
f=0
conn.send(file_data,f)
# print("data is send")
conn.close

