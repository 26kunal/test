from flask import Flask, flash,render_template,redirect,url_for,request
import os
import socket
import pickle
from werkzeug.utils import secure_filename

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
# @app.route('/test')
# def new():
#     return render_template('new.html')
# @app.route('/login',methods=["POST","GET"])
# def login():
#     if request.method=="POST":
#         user= request.form["nm"]
#         return redirect(url_for('user',usr=user))
#     else:
#         return render_template('login.html')
app.config["SECRET_KEY"]="hello"
upload="C:/Users/admin/Desktop/faltuuuuuuu/igaccount/server"
app.config["FILE_UPLOAD"]=upload
app.config["ALLOWED_EXTENSION"]=["csv","txt"]
app.config["MAX_FILESIZE"]= 16*1024*1024
def allowed_files(filename):
    if not "." in filename:
        return False
     
    ext=filename.rsplit(".",1)[1].lower()
    if ext not in app.config["ALLOWED_EXTENSION"]:
        return int(0)
    elif ext=='txt':
        return int(1)
    else:
        return int(2)
def allowed_size(filesize):
    if int(filesize) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False  
@app.route('/file',methods=["POST","GET"])
def file():
  
    if request.method=="POST":
        if request.files:
            if not allowed_size(request.cookies.get("filesize")):
                flash("File Size Must Be Less Than 16MB")
                return redirect(request.url)


            file_name = request.files["file"]
            if file_name.filename=="":
                flash("File must have a name")
                return redirect(request.url)
            k=allowed_files(file_name.filename)
            print("kunal")
            if k==0:
                flash("File Extenstion must be either '.txt' or '.csv'")
                return redirect(request.url)
            else:
                file_name.filename=secure_filename(file_name.filename)
                file_name.save(os.path.join(app.config["FILE_UPLOAD"],file_name.filename))
                   
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host=socket.gethostname()
           
            port=5000
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host,port))
            s.listen(1)
            print(host)
            print("waiting for connection")
            conn, addr= s.accept()
            print(addr, "has connected!")
            # filename=input(str("enter filename"))
            file=open(file_name.filename,'rb')
            file_data=file.read(80000)
        
            conn.send(file_data)
            print("data is send")
            flash("File has been uploaded successfully")
        
            return redirect(request.url)
            # conn.close
    print("get")   
    return render_template("file.html")
    
        
# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"


# @app.route('/<name>')
# def user(name):
#     return "hello"+name
# @app.route('/admin')
# def admin():
#     return redirect(url_for('user',name="user!"))


if __name__ == '__main__':

    app.run(debug=True)