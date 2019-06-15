import os, sys
from flask import Flask, render_template, request, url_for, redirect, jsonify
#import pandas as pd

from backend.MainApp import *

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
champions = dict()
user_name = ''
error_flag = False
@app.route('/', methods = ['GET', 'POST'])
def index():
	global champions
	global user_name
	global error_flag
	url= request.url
	print(url)
	if url[-1] == '/':
		user_name = ''
		champions = []
		error_flag = False

	c = ChampionRecommender()
	if request.method == "POST":
		user_name = request.form['username']
		try:
			error_flag = False
			champions, _ = c.recommender(user_name)
			champions = list(champions.keys())
			return redirect(url_for('index', user_name = user_name))
		except Exception as e:
			user_name = ''
			error_flag = True
			champions = []
			return redirect(url_for('index', error_flag = error_flag))

	return render_template('index.html', user_name = user_name, champions = champions, error_flag = error_flag)

@app.route('/all_network')
def all_network():
	return render_template('all_network.html')

@app.route('/top_network')
def top_network():
	return render_template('top_network.html')

@app.route('/jungle_network')
def jungle_network():
	return render_template('jungle_network.html')

@app.route('/middle_network')
def middle_network():
	return render_template('middle_network.html')

@app.route('/bottom_network')
def bottom_network():
	return render_template('bottom_network.html')

@app.route('/support_network')
def support_network():
	return render_template('support_network.html')


if __name__ == '__main__':
    app.run()


