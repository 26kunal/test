from flask import Flask, redirect, render_template,request,url_for
import os
import socket
app = Flask(__name__)
# @app.route("/client")
# def client():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # host = input(str("please enter host address: "))
#     port=5000
#     s.connect((socket.gethostname(),port))
#     print("connected")
#     return
    
@app.route("/")
def home():
    s=socket.socket()
    host=socket.gethostname()
    port=5000
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(1)
    print(host)
    print("waiting for connection")
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = input(str("please enter host address: "))
    # port=5000
    ss.connect((socket.gethostname(),port))
    # return redirect(url_for("client"))
    conn, addr= s.accept()
    print(addr, "has connected!")
    return "hello"#redirect(request.url)
if __name__ == '__main__':
	app.run(debug=True)