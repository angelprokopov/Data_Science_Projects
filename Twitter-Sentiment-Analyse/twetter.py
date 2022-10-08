import tweepy

consumer_key = "jgDAFJyEXSNawIEHJn0lnR27A"
consumer_secret = "zLAGXso6zgFGuKN7astwhM5v5hxoKym84Kkek0j41hDOWjJoJ2"
access_key = "2333961427-xJOgQGlS9FZRyaJHuZBb8aQXlXvxO4Ysx3TnL6B"
access_secret = "pWgd5QoXZMXX8qZig5NWEb1lE4lTsessbGvDXMnEfiN1b"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key,access_secret)
api = tweepy.API(auth)

tweets = api.search_tweets(q='JusticeForJohnnyDepp', count=99000)
for tweet in tweets:
    print (tweet.text)