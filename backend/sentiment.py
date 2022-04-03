import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import twitter_client as tc
import flask as fl

def clean_tweet( tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment( tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


def final(cont):
        parsed_list = []
        for tweet in cont:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet['full_text']
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet['full_text'])
            parsed_list.append(parsed_tweet)

        return parsed_list
