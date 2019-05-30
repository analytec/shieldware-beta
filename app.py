from flask import *
import twitterdata
import engine
from flask import Flask, request, jsonify
import csv_utils
from csv_utils import *
import os
from werkzeug.utils import secure_filename
from flask_basicauth import BasicAuth
import creds

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = creds.auth_token_penult
app.config['BASIC_AUTH_PASSWORD'] = creds.auth_token_prelim
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

@app.route('/', methods=['GET', 'POST'])
@basic_auth.required
def home():
    error=None
    if request.method == 'POST':
        error=None
        file = request.files['file']
        filename = secure_filename(file.filename)

        file.save(os.path.join('csv/', filename))
    return render_template('home.html', error=error)

@app.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_display():
    error=None
    if request.method == 'POST':
        error=None
        processor_count = int(request.form['processor-count'])
        try:
            tweets_num = int(request.form['tweets-num'])
        except Exception as e:
            return render_template('home.html', errorcsv="Please select a valid number of tweets.")
        try:
            selected_file = request.files['file']
        except Exception as e:
            return render_template('home.html', errorcsv='Please select a CSV file to use.')
        filename = secure_filename(selected_file.filename)
        if filename.endswith(".csv") == False:
            error = "Please select a .csv file!"
            return render_template('home.html',errorcsv=error)
        else:
            selected_file.save(os.path.join('csv/', filename))

        usernames = csv_to_list('csv/' + filename)
        for individual_username in usernames:
            if engine.check_user_exists(individual_username):
                print(individual_username + " exists!")
            else:
                error_msg = str(individual_username) + " does not exist!"
                return render_template('home.html', errorcsv=error_msg)
                break
        try:
            engine.twitter_bulk_query_wad(usernames, tweets_num=tweets_num, threads=processor_count)
        except Exception as e:
            print(e)
            return render_template('error_page.html', error=str(e))
        username_count = len(usernames)
        div_size = username_count*20 + 10
        return render_template('dashboard.html', usernames = usernames, div_size=div_size)


@app.route('/data', methods=['GET','POST'])
def data():
    error=None
    if request.method == 'POST':
        error=None
        username = str(request.form['username-tw'])
        try:
            tweets_num = int(str(request.form['tweets-num']))
            processor_count = int(request.form['processor-count'])
        except Exception as e:
            return render_template('home.html', error="Please enter a valid number of tweets and a valid processor count.")
        if not username:
            error = "Please enter a username before searching!"
            return render_template('home.html', error=error)
        if not engine.check_user_exists(username):
            error = "Twitter user does not exist!"
            return render_template('home.html', error=error)
        try:
            result = engine.concurrent_twitter_query_wad(username, tweets_num=tweets_num, threads=processor_count)
        except Exception as e:
            print(e)
            return render_template('error_page.html', error=str(e))
        print(engine.all_data)
        return redirect(url_for('tw_graph', username=username))

@app.route('/tw_graph/<username>', methods=['GET', 'POST'])
def tw_graph(username):
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
