import redis
import time

conn = redis.Redis(port=6788)

while True:

    cities = conn.keys()

    for city in cities:

        d = conn.hgetall(city)

        for loc in d:
            if int(d[loc]) > 1:
                count = int(d[loc])
                count -= 1
                d[loc] = str(count)

        conn.hmset(city,d)

    time.sleep(2)

