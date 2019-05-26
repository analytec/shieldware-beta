import multiprocessing as mp
import twitterdata
import engine
import csv_utils
import time

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
    results = pool.map(twitter_query_wad, user_list)

    print('twitter_bulk_query_wad() completed.')
    return results

print('\n\n*******************FINAL RESULTS******************************\n')
result = twitter_bulk_query_wad(['narendramodi', 'POTUS'])
print('Finished')
print(result)
