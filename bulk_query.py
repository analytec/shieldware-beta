import multiprocessing as mp
import twitterdata
import engine
import csv_utils
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

def twitter_query_wad(username):
    all_tweets = twitterdata.get_all_tweets(username)
    tweets_output = engine.getOutput(all_tweets)
    weapon_vals = engine.checkWeapons(tweets_output)
    alcohol_vals = engine.checkAlcohol(tweets_output)
    drug_vals = engine.checkDrugs(tweets_output)
    
    print('Data acquired for user: ' + username)
    return ({
        'weapons' : weapon_vals,
        'alcohol' : alcohol_vals,
        'drugs'   : drug_vals
    })

# twitter_bulk_query_wad() - process and return the Weapons/Alcohol/Drugs content of multiple Twitter usernames
def twitter_bulk_query_wad(user_list, threads=2):
    print(user_list)

    pool = mp.Pool(threads)
    pool_results = pool.map(twitter_query_wad, user_list)
    results = [{user_list[i] : pool_results[i]} for i in range(len(user_list))]

    print('twitter_bulk_query_wad() completed.')
    return results

print('\n\n*******************FINAL RESULTS******************************\n')
result = twitter_bulk_query_wad(csv_utils.csv_to_list('csv/accounts.csv'), 4)
print('Finished')
pp.pprint(result)
