# from config.keys import access_token_key,access_token_secret,consumer_secret,consumer_key
import redis
import pprint
import time
import json
import numpy
import sys
from TwitterAPI import TwitterAPI
''' adapted from mike's tutorials'''

''' These are my authentication tokens required to access the Twitter API.
    Anyone who wants to create an application using Twitter's API needs to get
    approved access through these keys and secrets '''
access_token_key = "28203065-AzK05fKKF4OzmPE0m1PbdZTq0vj4lsogO8JXWxXLH"
access_token_secret = "q6j4iDDMqbsiY3LJTZXd1SCQ1RHgNZTQbQw1tcwpO9LDO"
consumer_secret = "b6eIYasgVwIu3cskn3a8omPwms5S216i2G9OaBURYRQCFSM9Rd"
consumer_key = "sXYl8MLLMnfE7HCl9lIZ3ytEl"

''' This is where we connect to the Twitter API using a python wrapper called TwitterAPI, which we
 imported above. (If you would like more information on TwitterAPI, the docs and other usage info
  is available at [https://github.com/geduldig/TwitterAPI](https://github.com/geduldig/TwitterAPI).)
  I am using the recommended wrapper suggested by the Twitter API, and I think this is an easier way
  to interface with the API. '''
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

''' This connects to a key value store called Redis, which we imported above. We will be using this later
    in order to store all of the time deltas since each message occured in our stream so that we can calculate
    the average rate of our stream. It's good to have something like this instead of a heavier database
    that takes extra setup and configuration.'''
# conn = redis.Redis()
''' This parameter sets the initial state of last which is necessary for starting to gauge time-deltas (change in time since we saw the last message from our stream). The first time delta will not have a previous value to check against, so we will start w/ zero then start subtracting the last value we had for the time to get an adequate time-delta '''
last = 0
while True:
    ''' These two variables below, TERM and LOCATION refer to what word we are searching for in the tweets as well
    as what Latitude and Longitude that tweet came from. I chose New York City's coordinates and the search term `weather` in order to see if people are talking more and more about the weather '''
    TERM = 'weather'
    LOCATION = '-74,40,-73,41'
    # print "searching for {} in NYC".format(TERM)

    ''' This is using the wrapper's api language and requesting to get a stream of tweets with the specified search conditions:TERM and LOCATION that are described above. r is a list of objects'''
    r = api.request('statuses/filter', {'track':TERM})

    ''' Here we iterate each tweet we received from our request to the Twitter api based on the search conditions. I am creating a dictionary object that we can process as JSON later and that contains crucial information about each tweet. We have `time` for the time on our system in which we processed the tweet. We have this information to check for time-deltas later in order to check what the rate of the stream was. Then we add the tweet contents in `tweet` just to get a visual understanding of what is being tweeted and what kind of `weather` this Twitter user was writing a Tweet about. We also store `created_at` for no reason other than correlating the time something was tweeted in real time. I use the `.encode(utf-8)` since some tweets or data from twitter have interesting characters that are harder to process with JSON.'''
    weather_tweets = []
    pp = pprint.PrettyPrinter(indent=4)

    for item in r:
      if item.get("place",None) is not None:
        d = {"time": time.time(), "city": str(item["place"]["full_name"]), "retweets": str(item["retweet_count"]),  "tweet": str(item["text"].encode('utf-8')), "created_at": str(item["created_at"].encode('utf-8'))}
        if d:
          weather_tweets.append(d)
          print json.dumps(d)


      '''We need to flush our standard output'''
      sys.stdout.flush()
    time.sleep(5)
