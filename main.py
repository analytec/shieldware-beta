from flask import *
import twitterdata

from engine import
from flask import Flask, request, jsonify
import csv_utils
from csv_utils import *
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('csv/', filename))
    return render_template('home.html', title='Home')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_display():
    if request.method == 'POST':
        usernames = []
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('csv/', filename))
        bulk_dict = twitter_bulk_query_wad(csv_to_list('csv/' + filename), threads=4)

        return render_template(
            'tw_graph.html',
            name = username,
            drug_vals = drug_vals,
            weapon_vals = weapon_vals,
            alcohol_vals = alcohol_vals,
            x_vals = x_vals
        )

@app.route('/tw_graph', methods=['GET', 'POST'])
def tw_graph():
    if request.method == 'POST':
        '''username = str(request.form['username-tw'])
        all_tweets = twitterdata.get_all_tweets(username)
        tweets_output = engine.getOutput(all_tweets)
        print("Getting drug vals...")
        drug_vals = engine.checkDrugs(tweets_output)
        print("Getting weapon vals...")
        weapon_vals = engine.checkWeapons(tweets_output)
        print("Getting alcohol vals...")
        alcohol_vals = engine.checkAlcohol(tweets_output)'''
        x_vals = engine.gen_list(10)
        username = str(request.form['username-tw'])
        data = all_data[username]
        return render_template(
            'tw_graph.html',
            name = username,
            drug_vals = drug_vals,
            weapon_vals = weapon_vals,
            alcohol_vals = alcohol_vals,
            x_vals = x_vals
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8080)
