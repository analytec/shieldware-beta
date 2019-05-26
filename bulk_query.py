from multiprocessing import Process, Lock
import twitterdata
import engine
import csv_utils
import time

lock = Lock()

# twitter_bulk_query_wad() - process and return the Weapons/Alcohol/Drugs content of multiple Twitter usernames
def twitter_bulk_query_wad(user_list):
    print(user_list)
    results = {}

    def twitter_query_wad(username):
        all_tweets = twitterdata.get_all_tweets(username)
        tweets_output = engine.getOutput(all_tweets)
        weapon_vals = engine.checkWeapons(tweets_output)
        alcohol_vals = engine.checkAlcohol(tweets_output)
        drug_vals = engine.checkDrugs(tweets_output)
        lock.acquire()
        try:
            results[username] = {
                'weapons' : weapon_vals,
                'alcohol' : alcohol_vals,
                'drugs'   : drug_vals
            }
        finally:
            lock.release()
        print(results)
        print('Results acquired for user ' + username)

    for element in user_list:
        user_process = Process(target=twitter_query_wad, args = (element,))
        user_process.start()
    while len(results) < len(user_list):
        print(str(len(results)) + ' results gathered so far.')
        time.sleep(1)
    print('twitter_bulk_query_wad() completed.')
    return results

print('\n\n*******************FINAL RESULTS******************************\n')
result = twitter_bulk_query_wad(['narendramodi', 'POTUS'])
print('Finished')
print(result)
