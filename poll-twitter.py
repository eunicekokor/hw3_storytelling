from config.secrets import *
import redis
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
conn = redis.Redis()
''' This parameter sets the initial state of last which is necessary for starting to gauge time-deltas (change in time since we saw the last message from our stream). The first time delta will not have a previous value to check against, so we will start w/ zero then start subtracting the last value we had for the time to get an adequate time-delta '''
last = 0
while True:
    ''' These two variables below, TERM and LOCATION refer to what word we are searching for in the tweets as well
    as what Latitude and Longitude that tweet came from. I chose New York City's coordinates and the search term `weather` in order to see if people are talking more and more about the weather '''
    TERM = 'weather'
    LOCATION = '-74,40,-73,41'
    # print "searching for {} in NYC".format(TERM)

    ''' This is using the wrapper's api language and requesting to get a stream of tweets with the specified search conditions:TERM and LOCATION that are described above. r is a list of objects'''
    r = api.request('statuses/filter', {'track': TERM, 'locations':LOCATION})

    ''' Here we iterate each tweet we received from our request to the Twitter api based on the search conditions. I am creating a dictionary object that we can process as JSON later and that contains crucial information about each tweet. We have `time` for the time on our system in which we processed the tweet. We have this information to check for time-deltas later in order to check what the rate of the stream was. Then we add the tweet contents in `tweet` just to get a visual understanding of what is being tweeted and what kind of `weather` this Twitter user was writing a Tweet about. We also store `created_at` for no reason other than correlating the time something was tweeted in real time. I use the `.encode(utf-8)` since some tweets or data from twitter have interesting characters that are harder to process with JSON.'''
    for item in r:
      d = {"time": time.time(), "tweet": str(item["text"].encode('utf-8')), "created_at": str(item["created_at"].encode('utf-8'))}
      # print d

      ''' This is the condition that is triggered initially. We can now store the last value we had for the time so we can calculate the `time-delta` I described above named `delta`'''
      if last == 0:
          last = d["time"]
          continue
      ''' Calculating the time-delta'''
      delta = d["time"] - last
      # print {"time": d["time"], "delta": delta}

      ''' Using the Redis Connection, now we are going to enter this into our key-value store. We set the data that we got and assigned them to d['time']=key, delta=value, and 5 to be an interesting rate'''
      conn.setex(d["time"], delta, 5)
      keys = conn.keys()
      values = conn.mget(keys)

      ''' Now we are about to calculate the average rate, which is the average of each of the time differences.'''
      try:
          deltas = [float(v) for v in values]
      except TypeError:
          print keys
          continue
      ''' If we have more than 0 deltas, we can calculate an average. Here we do. '''
      if len(deltas):
        rate = sum(deltas)/float(len(deltas))
      else:
        rate = 0

      ''' Now we store the rate and store the default Exciting value '''
      d["rate"] = rate
      d["exciting"] = False


      # print json.dumps({"rate":rate})
      '''I chose a rate of streams that after testing different values, thought this would give adequate
      notice that right now the rate is `excited` or has a lot more activity than usual. Even though .17 is
      very arbitrary, I still saw a lot of interesting data based on this!'''
      if rate <= .17:
        # print "the {} is really exciting people right now!".format(TERM)
        d["exciting"] = True
      print json.dumps(d)

      last = d["time"]

      '''We need to flush our standard output'''
      sys.stdout.flush()

    delta_t = numpy.random.exponential(5)
    time.sleep(delta_t)
