#!/bin/bash


./consume-1.usa.gov.sh | python insert_referrer_by_city.py &
python decrementer.py &
python city-bot-api.py &
