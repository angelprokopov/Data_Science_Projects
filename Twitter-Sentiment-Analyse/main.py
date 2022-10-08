import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer

data = pd.read_csv("justiceforjohnnydepp.csv")
stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))


def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text


data["tweet"] = data["tweet"].apply(clean)
sentiment = SentimentIntensityAnalyzer()
data["Positive"] = [sentiment.polarity_scores(i)["pos"] for i in data["tweet"]]
data["Negative"] = [sentiment.polarity_scores(i)["neg"] for i in data["tweet"]]
data["Neutral"] = [sentiment.polarity_scores(i)["neu"] for i in data["tweet"]]

data = data[["tweet", "Positive",
             "Negative", "Neutral"]]
print(data.head())

x = sum(data["Positive"])
y = sum(data["Negative"])
z = sum(data["Neutral"])


def sentiment_score(a, b, c):
    if b > a > c:
        print("Positive")
    elif b > a > c:
        print("Negative")
    else:
        print("Neutral")


sentiment_score(x, y, z)

print("Positive: ", x)
print("Negative: ", y)
print("Neutral: ", z)