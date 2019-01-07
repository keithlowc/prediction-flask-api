from flask import Flask, jsonify, request
from flask_cors import CORS
from run_rnn import *

from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return '''<h1>Ecovisor Analysis </h1> 
    <ul>
	    <li>
	    	<p>This Recurrent Neural Network predicts the closing price of a stock - for <b>T+1</b></p>
	    </li>
	    <li>
	    	<p>1 - To run RNN do the following <b>url/prediction/ticker</b> - Make sure the ticker is in the yahoo finance api</p>
	    </li>
        <li>
            <p>2 - Once you run step <b>#1</b> it will return an <b>ID_Value</b>, copy that value and create the new url (<b>url/results/ID_Value</b> it takes like 10 seconds to show the real value)</p>

        </li>
    	<h2>Notes:</h2>
    	<li>
    		<p>The request may take up to 10 seconds - So be kind and wait :)</p>
    	</li>
    	<li>
    		<p>The request may time out - Please try again with a different ticker <b>AMD is known to have this issue</b></p>
    	</li>
    	<h2>Description:</h2>
    	<li>
    		<p><b>Ticker:</b> Ticker of stock</p>
    	</li>
    	<li>
    		<p><b>Today:</b> Current price of stock from yahoo finance api</p>
    	</li>
    	<li>
    		<p><b>Tomorrow predicted:</b> Stock price prediction of T+1</p>
    	</li>
    	<li>
    		<p><b>Percentage Difference:</b> If positive value then take as gain of 1 day to another. If negative value take as loss</p>
    	</li>

    	<h2>Tested tickers - All of these are known to work!</h2>
    	<li>
    		<p>FB</p>
    	</li>
    	<li>
    		<p>AAPL</p>
    	</li>
    	<li>
    		<p>NFLX</p>
    	</li>
    	<li>
    		<p>GOOGL</p>
    	</li>

	</ul>'''

@app.route('/test/<ticker>', methods=['GET'])
def get_test(ticker):
	return jsonify({'ticker': ticker})

q = Queue(connection=conn)

@app.route('/prediction/<ticker>', methods=['GET','POST'])
def get_prediction(ticker):

    ticker = ticker
    job = q.enqueue_call(
        func = rq_test_func, args=(ticker,), result_ttl=5000
    )
    return jsonify(
        {
            'id': str(job.id)
        })

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        today = job.result[0]
        tommorrow = job.result[1]
        difference = job.result[2]
        ticker = job.result[3]
        return jsonify(
            {
                'ticker': str(ticker.upper()),
                'today': float(today),
                'tommorrow': float(tommorrow),
                'percentage_difference': float(difference), 
            })
    else:
        return jsonify({
                'Message': "The job is still running - try again in a few seconds",
            })

if __name__ == '__main__':
	app.run(debug=True)
	# To be able to request this api do
	# import requests
	# x = requests.get('url')
	# val = x.json()
	# print(val['ticker'])