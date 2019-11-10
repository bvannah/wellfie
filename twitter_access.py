#thanks to https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python//

import re 
import tweepy 
from tweepy import OAuthHandler
from tweepy import API
import twitter
import sys

def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", str(tweet)).split()) 

def getTweets(handle):
        consumer_key = 'USE'
        consumer_secret = 'YOUR'
        access_token = 'API'
        access_token_secret = 'KEYS'
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        new_tweets = api.user_timeline(screen_name = handle, count=10000)

        tweets = [tweet.text for tweet in new_tweets] #.encode("utf-8") for tweet in new_tweets]
        tweetString = ""
        for s in tweets:
                for c in s:
                        if ord(c)<128:
                                tweetString+= str(c)

                tweetString += " "
        return tweetString


if __name__ == "__main__": 
    # calling main function 
    print(getTweets("NICKIMINAJ"))

