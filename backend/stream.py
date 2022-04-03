import keys
import tweepy
import twitter_client as tc
import json
from info import data
#from tweepy.streaming import StreamListener
from flask_cors import CORS
auth = tweepy.OAuthHandler(keys.consumer_key(), keys.consumer_secret())
auth.set_access_token(keys.access_token(), keys.access_token_secret())
#oggetto API per interazione con twitter
api = tweepy.API(auth)


class Streamer(tweepy.Stream):

    
    def on_status(self, status):
        
        t=dictify_single_tweet(status)
        data.append(t)
        #aggiungo ogni tweet che arriva alla lista globale
        
    def on_error(self, status):
        print(status)
        

# Initialize instance of the subclass


"""def stop():
    streamer.continua=False
"""



# Filter realtime Tweets by keyword
def use_stream ():
    query="ucraine"
    streamer = Streamer(
        keys.consumer_key(), keys.consumer_secret(),
        keys.access_token(), keys.access_token_secret()
    )

    try:
        streamer.filter(track=["ucraine", "giveaway", "war", "putin", "nato", "usa", "milan", "roma"])
        
    except Exception:
        pass

  


def dictify_single_tweet(tweet):
    """ Ritorna una rappresentazione in forma di dizionario di python
        dello status di tweet"""
    
    
    tweet_dict = {}
    tweet_dict['user'] = tc.dictify_user(tweet.user)
    tweet_dict['place'] = tc.dictify_place(tweet.place)
    
    if tc.is_retweet(tweet):
        tweet_dict['retweeted_status'] = dictify_single_tweet(
            tweet.retweeted_status)
    else:
        tweet_dict['full_text'] = tweet.text
        print(tweet.text)
        print("//////")

    return tweet_dict


def listify_tweets(tweets) :
    """ Ritorna una rappresentazione in forma di dizionario di python
        di tweets. Il dizionario è indicizzato su interi da 0 a n come
        fosse una lista"""
    tweets_list = []

    for tweet in tweets:
        tweet_dict = dictify_single_tweet(tweet)
        tweets_list.append(tweet_dict)


    return tweets_list

