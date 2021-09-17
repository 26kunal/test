import string
from collections import Counter

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import socket
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = input(str("please enter host address: "))
port=5000
s.connect((socket.gethostname(),port))
print("connected")
file_data=(s.recv(80000))

filename="data.txt"
# if int(file_data[1])==48:
#     filename="data.txt"
# else:
#     filename="data.csv"
file=open(filename,'wb')

file.write(file_data)
file.close()
print("recieved")

text = open(filename, encoding='utf-8').read()
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
def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")


sentiment_analyse(cleaned_text)

fig, ax1 = plt.subplots()
ax1.bar(count.keys(), count.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()