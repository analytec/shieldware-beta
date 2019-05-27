from flask import *
import twitterdata
import engine
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


@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == 'POST':
        username = str(request.form['username-tw'])
        all_tweets = twitterdata.get_all_tweets(username)#
        x_vals = engine.gen_list(10)
        username = str(request.form['username-tw'])
        data = engine.all_data[username]
        return redirect(url_for('tw_graph',username=username)

@app.route('/tw_graph', methods=['GET', 'POST'])
def tw_graph(username):
    #if request.method == 'POST':
    username = str(request.form['username-tw'])
    x_vals = engine.gen_list(10)
    data = engine.all_data[username]
    return render_template(
        'tw_graph.html',
        name = username,
        drug_vals = data['drugs'],
        drug_max = max(data['drugs']),
        weapon_vals = data['weapons'],
        weapon_max = max(data['weapons']),
        alcohol_vals = data['alcohol'],
        alcohol_max = max(data['alcohol']),
        x_vals = x_vals
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8080)
