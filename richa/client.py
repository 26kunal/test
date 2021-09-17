import socket
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = input(str("please enter host address: "))
port=5000
s.connect((socket.gethostname(),port))
# print("connected")
file_data=(s.recv(1024))


if int(file_data[1])==48:
    filename="abc.csv"
else:
    filename="abc.txt"
file=open(filename,'wb')

file.write(file_data)
file.close()
# print("recieved")