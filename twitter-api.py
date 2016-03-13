''' Based upon Mike's Demo at https://github.com/mikedewar/RealTimeStorytelling/'''

import flask
from flask import request
import redis
import collections
import json
import numpy as np
rate = None
# This creates a Flask instance to host our API
app = flask.Flask(__name__)
# To get our data, we have to pull from our redis information
conn = redis.Redis(port=6788)

def buildHistogram():
    # Getting all the city names and the values and returning a histogram representing
    # The distribution of how many counts we have per city
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(c.values())
    print values
    for k,v in c.items():
      print v/float(z)

    return {k:v/float(z) for k,v in c.items()}

# This fetches current rate, which is a global variable created as the stream is coming in
# But is accessible from this function
# @app.route("/rate")
# def get_rate():
#   return rate

# This is the route that creates the histogram and displays it on the screen
@app.route("/")
def histogram():
    h = buildHistogram()
    return json.dumps(h)

@app.route("/entropy")
def entropy():
    h = buildHistogram()
    return -sum([p*np.log(p) for p in h.values()])

@app.route("/probability")
def probability():
    city = request.args.get('city', '')
    rt = request.args.get('retweets', '')
    # get the distribution for the city
    print city
    d = conn.hgetall(city)
    # get the count for the referrer
    try:
      c = d[rt]
    except KeyError:
      return json.dumps({
        "city": city,
        "prob": 0,
        "retweets": rt
      })
    # get the normalising constant
    z = sum([float(v) for v in d.values()])
    return json.dumps({
      "city": city,
      "prob": float(c)/z,
      "retweets": rt
      })


if __name__ == "__main__":
    app.debug = True
    app.run()
