import json
import sys
import redis
import time
import urlparse

conn = redis.Redis(port=6788)
''' Based upon Mike's Demo at https://github.com/mikedewar/RealTimeStorytelling/'''
while 1:
    line = sys.stdin.readline()
    try:
        d = json.loads(line)
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

    conn.hincrby(city, rt, 1)
    print json.dumps({"city": city, "retweets": int(rt)})
    sys.stdout.flush()
