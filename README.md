# hw3_storytelling

## About
This is tracking distributions of tweets from different locations that are about the term 'weather', but one can experiment with different specific weather related queries like 'sunny' or 'rain'

These are from Twitter, a social media platform that provides user generated <140 character blurbs in realtime.

I have always wondered if other people tweeted about the weather if there was something significant happening especially in different locations. I know definitely do. So I wanted to track which places use Twitter more for things like weather, and maybe learn something about places where people tweet and if communities are more likely to use social media as a tool for information distribution.

My alerting system alerts when there is a change in entropy above .5. It seemed like mrore people were active after this threshold.

**API Used:** Twitter API through Python wrapper TwitterAPI If you would like more information on TwitterAPI, the docs and other usage info is available at https://github.com/geduldig/TwitterAPI.


## File Overviews
### `poll-twitter.py`
This creates the twitter stream and returns JSON about the number of followers and retweets.
### `numbers-by-weather.py`
This inserts our numbers into the Redis Server as key value pairs.
### `decrement.py`
This decrements counts so we can always maintain a current level of data saturation.
### `twitter-api.py`
This is our server which can access information based on data collected in our server.

## How to Run
- 1. Run a Redis Server in One Window
`redis-server --port=6788`
- 2. Run the script to poll data, insert and upkeep data, and publish it to our API
`python poll-twitter.py | python numbers-by-weather.py & python decrement.py & python twitter-api.py`
