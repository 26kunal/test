from flask import Flask, redirect, render_template,request
import os
import socket
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")


app.config["FILE_UPLOADS"] = "C:/Users/lenovo/OneDrive/Desktop/flask/uploads"

@app.route("/upload", methods=["GET","POST"])
def upload():
	if request.method == "POST":
		if request.files:
			image = request.files["image"]
			image.save(os.path.join(app.config["FILE_UPLOADS"], image.filename))
			

			s=socket.socket()
			host=socket.gethostname()
			port=5000
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind((host,port))
			s.listen(1)
			print(host)
			print("waiting for connection")
			conn, addr= s.accept()
			print(addr, "has connected!")
			file=open(image.filename,'rb')
			file_data=file.read(1024)
			conn.send(file_data)
			print("data is send")



			print("image is saved")
			return redirect(request.url)

	return render_template("upload.html")


if __name__ == '__main__':
	app.run(debug=True)