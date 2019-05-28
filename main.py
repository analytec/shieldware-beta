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
    error=None
    if request.method == 'POST':
        error=None
        file = request.files['file']
        filename = secure_filename(file.filename)

        file.save(os.path.join('csv/', filename))
    return render_template('home.html', title='Home', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_display():
    if request.method == 'POST':
        processor_count = int(request.form['processor-count'])
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('csv/', filename))
        usernames = csv_to_list('csv/' + filename)
        engine.twitter_bulk_query_wad(usernames, threads=processor_count)
        return render_template('dashboard.html', usernames = usernames)


@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == 'POST':
        username = str(request.form['username-tw'])
        if not username:
            error = "Please enter a username before searching!"
            return render_template('home.html', error=error)
        elif not engine.check_user_exists(username):
            error = "Twitter user does not exist!"
            return render_template('home.html', error=error)
        result = engine.concurrent_twitter_query_wad(username, threads=6)
        print(engine.all_data)
        return redirect(url_for('tw_graph', username=username))

@app.route('/tw_graph/<username>', methods=['GET', 'POST'])
def tw_graph(username):
    #if request.method == 'POST':
    x_vals = engine.gen_list(11)
    data = engine.all_data[username]
    print('WEAPON MAX: ' + str(max(data['weapons'])))
    print('DRUGS MAX: ' + str(max(data['drugs'])))
    print('ALCOHOL MAX: ' + str(max(data['alcohol'])))

    return  render_template(
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
    app.run(debug=True, host='localhost',port=8080)
