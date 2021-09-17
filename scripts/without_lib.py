import string
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# reading text file
text =open("example_data/read.txt",encoding="utf-8").read()
# print(text)

#converting into lower_case
lower_case = text.lower()
#print(lower_case)

#removing punctuations
cleaned_text = lower_case.translate(str.maketrans("","",string.punctuation))
#print(cleaned_text)

# splitting text into words
tokenized_words = cleaned_text.split()

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
# Removing stop words from the tokenized words list              
words = []
for word in tokenized_words:
    if word not in stop_words:
        words.append(word)
# print(words)

dict={}
with open('abriviation/abv.txt','r') as file:
    for line in file:
        clear_line=line.replace("\n",'')
        abv,full=clear_line.split(':')
        abv=abv.lower().strip()
        full=full.strip()
        dict[abv]=full

# print(dict)

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
    if word not in stop_words:
        final_words.append(word)
emotion_list = []
print(final_words)


# NLP Emotion Algorithm
# 1) Check if the word in the final word list is also present in emotion.txt
#  - open the emotion file
#  - Loop through each line and clear it
#  - Extract the word and emotion using split

# 2) If word is present -> Add the emotion to emotion_list
# 3) Finally count each emotion in the emotion list
emotion_list = []
with open('emotions/final_emotions.txt','r',encoding="utf-8") as file:
    for line in file:
        clear_line=line.replace("\n",'').replace(",",'').replace("'",'').strip()
        word,emotion=clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)
print(emotion_list)

with open('emotions/chat_emotions.txt','r',encoding="utf-8") as file:
    for line in file:
        clear_line=line.replace("\n",'').replace(",",'').replace("'",'').strip()
        word,emotion=clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)
# print(emotion_list)

count=Counter(emotion_list)
# print(count)

str=" "
str=str.join(final_words)
blob1=TextBlob(str)
print(format(blob1.sentiment))

blob2=TextBlob(str,analyzer=NaiveBayesAnalyzer())
print(format(blob2.sentiment))

# print(blob1.correct())

fig, ax1 = plt.subplots()
ax1.bar(count.keys(), count.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()