import multiprocessing as mp
import twitterdata
import csv_utils
import pprint
from sightengine.client import SightengineClient
from creds import client_access, client_key, all_creds
client = SightengineClient(client_access, client_key)

all_data = {}

def choose_api_key():
    global client
    for pair in all_creds:
        client = SightengineClient(pair[0], pair[1])
        result = client.check('wad').set_url('https://lh3.googleusercontent.com/-EL0JJV39VAs/XOyDvKml4NI/AAAAAAAADPA/QEYS42h75H0KvxzUToVi3kBGmqKzlNZtQCK8BGAs/s512/2019-05-27.jpg')['result']
        if result == 'success':
            print("Using API credentials " + str(pair))
            break

def getOutput(my_url_list):
    output_list = []
    result = None
    for my_url in my_url_list:
        output_list.append(client.check('wad').set_url(my_url))
    for output in output_list:  print(output)
    return output_list

def checkDrugs(output_list):
    my_drug_list = []
    for output in output_list:
        print(output)
        drugs = output['drugs']
        my_drug_list.append(drugs)
    return my_drug_list

def checkWeapons(output_list):
    my_weapon_list = []
    for output in output_list:
        weapons = output['weapon']
        my_weapon_list.append(weapons)
    return my_weapon_list

def checkAlcohol(output_list):
    my_alcohol_list = []
    for output in output_list:
        alcohol = output['alcohol']
        my_alcohol_list.append(alcohol)
    return my_alcohol_list

def gen_list(count):
    my_list = []
    for i in range(count):
        my_list.append(i)
    return my_list

pp = pprint.PrettyPrinter(indent=4)

# helper function - DO NOT use this outside this file
def wad_helper(output_list, query_type):
    results = []
    for output in output_list:
        print(output)
        res = output[query_type]
        results.append(res)
    return results

def concurrent_twitter_query_wad(username, threads):
    all_tweets = twitterdata.get_all_tweets(username)
    tweets_output = getOutput(all_tweets)
    pool = mp.Pool(threads)
    pool_results = pool.starmap(wad_helper, [(tweets_output, 'weapon'), (tweets_output, 'drugs'), (tweets_output, 'alcohol')])
    weapon_vals = pool_results[0]
    drug_vals = pool_results[1]
    alcohol_vals = pool_results[2]
    print('Data acquired concurrently for user: ' + username)
    result = {
        'weapons' : weapon_vals,
        'alcohol' : alcohol_vals,
        'drugs'   : drug_vals
    }
    all_data[username] = result
    return result


def twitter_query_wad(username):
    global all_data
    all_tweets = twitterdata.get_all_tweets(username)
    tweets_output = getOutput(all_tweets)
    weapon_vals = checkWeapons(tweets_output)
    alcohol_vals = checkAlcohol(tweets_output)
    drug_vals = checkDrugs(tweets_output)

    print('Data acquired for user: ' + username)
    result = {
        'weapons' : weapon_vals,
        'alcohol' : alcohol_vals,
        'drugs'   : drug_vals
    }
    all_data[username] = result
    return result

# twitter_bulk_query_wad() - process and return the Weapons/Alcohol/Drugs content of multiple Twitter usernames
# example usage: twitter_bulk_query_wad(['POTUS', 'narendramodi'], threads=4)
def twitter_bulk_query_wad(user_list, threads=2):
    print(user_list)

    pool = mp.Pool(threads)
    pool_results = pool.map(twitter_query_wad, user_list)
    results = [{user_list[i] : pool_results[i]} for i in range(len(user_list))]
    for element in results:
        for key in element:
            all_data[key] = element[key]

    print('twitter_bulk_query_wad() completed.')
    print("ALL DATA SO FAR: ")
    pp.pprint(all_data)
    return results
