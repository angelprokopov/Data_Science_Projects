import tweepy
import pandas as pd
import json
import csv
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import operator
import scipy
from skimage import io
from sklearn import *
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from textblob import TextBlob
from textblob import Word
from textblob.sentiments import NaiveBayesAnalyzer

# Authentication
consumer_key = "jgDAFJyEXSNawIEHJn0lnR27A"
consumer_secret = "zLAGXso6zgFGuKN7astwhM5v5hxoKym84Kkek0j41hDOWjJoJ2"
access_key = "2333961427-xJOgQGlS9FZRyaJHuZBb8aQXlXvxO4Ysx3TnL6B"
access_secret = "pWgd5QoXZMXX8qZig5NWEb1lE4lTsessbGvDXMnEfiN1b"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # Interacting with Twitter's API
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)  # Creating the API object

# Extracting Tweets
result = []
for tweet in tweepy.Cursor(api.search_tweets, q='jeffreydahmer', lang="en").items(2500):
    result.append(tweet)

print(type(result))
print(len(result))


def tweets_df(results):
    id_list = [tweet.id for tweet in results]
    data_set = pd.DataFrame(id_list, columns=["id"])
    data_set["text"] = [tweet.text for tweet in results]
    data_set["created_id"] = [tweet.created_at for tweet in results]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
    data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
    data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]

    return data_set


data_set = tweets_df(result)

# Remove tweets with duplicate text
text = data_set["text"]

for i in range(0, len(text)):
    txt = ' '.join(word for word in text[i].split() if not word.startswith('https:'))
    data_set._set_value(i, 'text2', txt)

data_set.drop_duplicates('text2', inplace=True)
data_set.reset_index(drop=True, inplace=True)
data_set.drop('text', axis=1, inplace=True)
data_set.rename(columns={'text2': 'text'}, inplace=True)

text = data_set["text"]

for i in range(0, len(text)):
    textB = TextBlob(text[i])
    sentiment = textB.sentiment.polarity
    data_set._set_value(i, 'Sentiment', sentiment)
    if sentiment < 0.00:
        SentimentClass = 'Negative'
        data_set._set_value(i, 'Sentiment', SentimentClass)
    elif sentiment > 0.00:
        SentimentClass = 'Positive'
        data_set._set_value(i, 'Sentiment', SentimentClass)
    else:
        SentimentClass = 'Neutral'
        data_set._set_value(i, 'Sentiment', SentimentClass)

Htag_df = pd.DataFrame()
j = 0

for tweet in range(0, len(result)):
    hashtag = result[tweet].entities.get('hashtags')
    for i in range(0, len(hashtag)):
        Htag = hashtag[i]['text']
        Htag_df._set_value(j, 'Hashtag', Htag)
        j = j + 1

# Join all the text from the tweets
Hashtag_Combined = " ".join(Htag_df['Hashtag'].values.astype(str))

no_jeffrey = " ".join([word for word in Hashtag_Combined.split()
                       if word != 'JeffreyDahmer'
                       and word != 'Dahmer'
                       and word != 'Netflix'
                       and word != 'serialkillers'
                       and word != 'truecrime'
                       and word != 'Evan Peters'
                       and word != 'truecrimecommunity'
                       ])
Tweet_mask = imageio.imread('twitter_mask.png')

# Create Word Cloud
wc = WordCloud(background_color="white", stopwords=STOPWORDS, mask=Tweet_mask)
wc.generate(no_jeffrey)
plt.imshow(wc)
plt.axis("off")
plt.savefig("C:\\Users\\Angel\\PycharmProjects\Hashtag_Analyse\\jeffreydahmer.png", dpi=300)
plt.show()

