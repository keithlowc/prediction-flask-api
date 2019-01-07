# Prediction Flask API

This api was created to allow users to use the a Machine Learning prediction model and the Yahoo finance api to predict the price of a stock and to be able to plot the trained values

## Needs:

* Redis queue 
* Redis Server
* A Worker (Follow the redis docs)

## Note: 

This is ready to be deployed onto Heroku. Also make sure to edit redis_url on worker.py to match your heroku Redis server id.

## Commands:

1 - redis-server
2 - python worker.py
3 - python main.py