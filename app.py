from flask import Flask, flash,render_template,redirect,url_for,request,session,send_file
import os
import socket
import pickle
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy



import string
from collections import Counter
import csv
import sys

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier



app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users1.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)


db = SQLAlchemy(app)

class users(db.Model):
	id1 = db.Column("id",db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	password = db.Column(db.String(100))
	email = db.Column(db.String(100))

	def __init__(self, name, password, email):
		self.name = name
		self.password=password
		self.email = email


@app.route("/home")
def home():
	return render_template("home.html")
@app.route("/view")
def view():
	return render_template("view.html",values=users.query.all())


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        pswd = request.form["pswd"]
        session["user"]=user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            if found_user.password == pswd:
                print("login successfull")
                # flash("login successfull")
                return redirect(url_for("loggedin"))
                
            else:
                flash("wrong PassWord")
                return redirect(url_for("login"))
        else:
            flash("wrong usrname")
            return redirect(url_for("login"))
    # elif "user" in session:
    #     flash("Already logged in")
    #     return redirect(request.url)
        # return render_template()
    else:
        return render_template("login.html")
        


@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        user= request.form["nm"]
        pswd = request.form["pswd"]
        email = request.form["email"]
        usr=users(user,pswd,email)
        db.session.add(usr)
        db.session.commit()
        flash("registered successful!!")
        return redirect(request.url)
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
	# flash("You have been logged out!", "info")
	session.pop("user", None)
	session.pop("email", None)
	return redirect(url_for("home"))
@app.route('/loggedin',methods=["POST","GET"])
def loggedin():
    print("loggedin")
    if request.method=="POST":
        print("post")
        return render_template('file.html')
    else:
        return render_template('loggedin.html')
app.config["SECRET_KEY"]="hello"
upload="C:/Users/admin/Desktop/faltuuuuuuu/igaccount"
app.config["FILE_UPLOAD"]=upload
app.config["MAX_FILESIZE"]= 16*1024*1024
def allowed_files(filename):
    if not "." in filename[0]:
        return False
     
    ext=filename[0].rsplit(".",1)[1].lower()
    if filename[1]==0:
        if ext == "txt":
            return True
        else:
            return False
    else:
        if ext == "csv":
            return True
        else:
            return False
        
    
def allowed_size(filesize):
    if int(filesize) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False 
def process(filename):
    test_str=" "
    text=""
    if allowed_files((filename,0)):
        text = open(filename, encoding='utf-8').read()
    else:
        temp_list=[]
        with open(filename,'r') as temp:
            temp_list=csv.reader(temp)
            for row in temp_list:
                
                test_str=test_str+" "+test_str.join(row)
                
        text=test_str
        
                
            
    # print(text)
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    # Using word_tokenize because it's faster than split()
    tokenized_words = word_tokenize(cleaned_text, "english")

    # Removing Stop Words 1
    words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            words.append(word)

    # Lemmatization - From plural to single + Base form of a word (example better-> good)
    lemma_words = []
    for word in words:
        word = WordNetLemmatizer().lemmatize(word)
        lemma_words.append(word)

    dict={}
    with open('abriviation/abv.txt','r') as file:
        for line in file:
            clear_line=line.replace("\n",'')
            abv,full=clear_line.split(':')
            abv=abv.lower().strip()
            full=full.strip()
            dict[abv]=full

    temp_words=[]

    for word in words:
        if word in dict.keys():
            temp_list=dict[word].split()
            for each in temp_list:
                temp_words.append(each.lower())
        else:
            temp_words.append(word)
        

    # Removing Stop Words 2
    final_words = []
    for word in temp_words:
        if word not in stopwords.words('english'):
            final_words.append(word)
    emotion_list = []
    print(final_words)
    with open('emotions/final_emotions.txt','r',encoding="utf-8") as file:
        for line in file:
            clear_line=line.replace("\n",'').replace(",",'').replace("'",'').strip()
            word,emotion=clear_line.split(':')

            if word in final_words:
                emotion_list.append(emotion)
    #print(emotion_list)
    with open('emotions/chat_emotions.txt','r',encoding="utf-8") as file:
        for line in file:
            clear_line=line.replace("\n",'').replace(",",'').replace("'",'').strip()
            word,emotion=clear_line.split(':')

            if word in final_words:
                emotion_list.append(emotion)
    # print(emotion_list)
    count=Counter(emotion_list)
    print(count)
    strr=" "
    strr=strr.join(final_words)
    # methode1
    blob1=TextBlob(strr)
    result=(format(blob1.sentiment))
    print(result)
    
    
    #methode2
    # blob2=TextBlob(str,analyzer=NaiveBayesAnalyzer())
    # print(format(blob2.sentiment))
    
    #methode3
    # def sentiment_analyse(sentiment_text):
    #     score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    #     if score['neg'] > score['pos']:
    #         print("Negative Sentiment")
    #     elif score['neg'] < score['pos']:
    #         print("Positive Sentiment")
    #     else:
    #         print("Neutral Sentiment")


    #sentiment_analyse(cleaned_text)

    fig, ax1 = plt.subplots()
    ax1.bar(count.keys(), count.values())
    fig.autofmt_xdate()
    plt.savefig('static/images/graph.png')
    print("saved")
    return result
   
   

@app.route('/test',methods=["POST","GET"])
def test():
  
    if request.method=="POST":
        if request.files:
            if not allowed_size(request.cookies.get("filesize")):
                flash("File Size Must Be Less Than 16MB")
                return redirect(request.url)


            file_name = request.files["file"]
            if file_name.filename=="":
                flash("File must have a name")
                return redirect(request.url)
            if not allowed_files([file_name.filename,0]):
                flash("File Extenstion must be '.txt'")
                return redirect(request.url)
                
            else:
                file_name.filename=secure_filename(file_name.filename)
                file_name.save(os.path.join(app.config["FILE_UPLOAD"],file_name.filename))
                # flash("THe File Has Been Uploded Successfully")
            result=process(file_name.filename)
            return render_template('result.html',result=result,flag=0)
        
            # return redirect(request.url)
            # conn.close
        else:
            return render_template("test.html")
    
    print("get")   
    return render_template("test.html")
    

@app.route('/download')
def download_file():
    p = "test.csv"
    return send_file(p, as_attachment=True)
def train_process(train,test):
    
    print("in train")
    train_text = []
    train_temp = []
    test_temp=[]
    result=[]
    
    with open(train,'r') as train_file:
        train_temp = csv.reader(train_file)
        cnt=0
        for row in train_temp:
            cnt=cnt+1
            tpl = ()
            if(row[1]==""):
                row[1]='neutral'
            tpl = (row[0],row[1])
            
            if cnt!=1:
                print(tpl)
                train_text.append(tpl)
    nbcl = NaiveBayesClassifier(train_text)
    with open(test,'r') as test_file:
        test_temp = csv.reader(test_file)
        cnt=0
        for row in test_temp:
            cnt=cnt+1
            temp=[]
            if cnt==1:
                temp.append("data")
                temp.append("result")
                result.append(temp)
            else:
                temp.append(row[0])
                temp.append(nbcl.classify(row[0]))
                result.append(temp)
    # print(result)
    with open(test, 'w') as result_file:
        writer = csv.writer(result_file)
        writer.writerows(result)
    return test
     

@app.route('/train',methods=["POST","GET"])
def train():
    if request.method == "POST":
        file_list=[]
        files = request.files.getlist("file")
        if len(files) != 2:
            flash("You need to upload exact two files. read instructions given below for help.")
            return redirect(request.url)
        for x in range(2):
            file=files[x]
            file_list.append(file.filename)
            print(file_list[x])
            if not allowed_size(request.cookies.get("filesize")):
                flash("File Size Must Be Less Than 16MB")
                return redirect(request.url)
            if file.filename=="":
                flash("File must have a name")
                return redirect(request.url)
            if not allowed_files([file.filename,1]):
                flash("File Extenstion must be '.csv'")
                return redirect(request.url)
            else:
                file.filename=secure_filename(file.filename)
                file.save(os.path.join(app.config["FILE_UPLOAD"],file.filename))
                flash("File "+file_list[x]+" Has Been Uploaded Successfully")
          
            
            
            # return render_template('result.html',result=result)
        
            # return redirect(request.url)
            # conn.close
        a=file_list[0]
        b=file_list[1]
        extra=[]
        f=0
        with open(a,'r') as var:
            extra = csv.reader(var)
            for row in extra:
                if(len(row)==1):
                    f=1
                    break
        if f==1:
            test=a
            train=b
        else:
            train=a
            test=b
        result=process(test)
        test=train_process(train,test)
        return render_template('result.html',result=result,flag=1)
        # file_name.save(os.path.join(app.config["FILE_UPLOAD"],file_name.filename))
        
        
    else:
        return render_template("train.html")
    
    print("get")   
    return render_template("train.html")
    
    

# @app.route('/<name>')
# def user(name):
#     return "hello"+name
# @app.route('/admin')
# def admin():
#     return redirect(url_for('user',name="user!"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)