import multiprocessing as mp
import twitterdata
import csv_utils
import pprint
from sightengine.client import SightengineClient
from creds import client_access, client_key
client = SightengineClient(client_access, client_key)


def getOutput(my_url_list):
    output_list = []
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

def twitter_query_wad(username):
    all_tweets = twitterdata.get_all_tweets(username)
    tweets_output = getOutput(all_tweets)
    weapon_vals = checkWeapons(tweets_output)
    alcohol_vals = checkAlcohol(tweets_output)
    drug_vals = checkDrugs(tweets_output)

    print('Data acquired for user: ' + username)
    return ({
        'weapons' : weapon_vals,
        'alcohol' : alcohol_vals,
        'drugs'   : drug_vals
    })

# twitter_bulk_query_wad() - process and return the Weapons/Alcohol/Drugs content of multiple Twitter usernames
# example usage: twitter_bulk_query_wad(['POTUS', 'narendramodi'], threads=4)
def twitter_bulk_query_wad(user_list, threads=2):
    print(user_list)

    pool = mp.Pool(threads)
    pool_results = pool.map(twitter_query_wad, user_list)
    results = [{user_list[i] : pool_results[i]} for i in range(len(user_list))]

    print('twitter_bulk_query_wad() completed.')
    pp.pprint(results)
    return results
