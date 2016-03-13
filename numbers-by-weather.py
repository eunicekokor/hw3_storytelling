''' Based upon Mike's Demo at https://github.com/mikedewar/RealTimeStorytelling/'''

import json
import sys
import redis
import time
import urlparse

''' This connects to a key value store called Redis, which we imported above. We will be using this later
    in order to store all of the time deltas since each message occured in our stream so that we can calculate
    the average rate of our stream. It's good to have something like this instead of a heavier database
    that takes extra setup and configuration.'''
conn = redis.Redis(port=6788)
''' Based upon Mike's Demo at https://github.com/mikedewar/RealTimeStorytelling/'''
while 1:
    line = sys.stdin.readline()
    try:
        d = json.loads(line)
        print d
    except ValueError:
        # sometimes we get an empty line, so just skip it
        continue

    try:
        city = d["city"]
    except KeyError:
        # if there is no city present in the message
        # then let's just ditch it
        continue

    try:
        rt = d["retweets"]
    except KeyError:
        # if there is no referrer present in the message
        # then let's just ditch it
        continue
    # This is importatnt and increments the
    conn.hincrby(city, int(rt), 1)

    keys = conn.keys()
    values = conn.mget(keys)
    # print keys
    # print values
    print json.dumps({"city": city, "retweets": int(rt)})
    sys.stdout.flush()
