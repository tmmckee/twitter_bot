import tweepy
import time
import random
from keys import *

#keys are imported from a seperate file above and then used below to
#so that we have access to the twitter development keys
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


FILE_NAME = 'last_seen_id.txt'

#this is the last_seen_id is retrieved from the text file with the same name
#and is then returned where it is then replaced with the newest id so that
#the bot is not responding to the same posts as before
def retrieve_last_seen_id(FILE_NAME):
    f_read = open(FILE_NAME, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, FILE_NAME):
    f_write = open(FILE_NAME, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
    
#this is where we will actually responding to users. first it checks for the 
# word "it" and then will respond based on that, or it will respond with 
# different phrases that are stored in a list    
def reply_to_tweets(): 
    last_seen_id = retrieve_last_seen_id(FILE_NAME)    
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')

    list1 = ['We are the knights that say.... NEE!!', 'We are the keepers of the sacred words: NEEE! PING! And NEEEE WOMMM!!',
    'NEEE! NEEE! NEeeEeEE!', 'We want.... A SHRUBBERY!', 'You must cut down the mightiest tree in the forest... WIIIIITHH.... A herring!!']

    for mention in reversed(mentions):
        print(str(mention.id) + ' ' + mention.full_text, flush=True)
        last_seen_id= mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if 'it' in mention.full_text.lower():
            print('found the word it!', flush=True)
            print('retaliating back...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' 'Do not say that word! ("it")')
            mention.favorite()
            mention.user.follow()
            
        else:
            print('challenger approaches!', flush=True)
            print('answering the challenge...', flush=True)
            rand = random.randint(0, 4)
            api.update_status(f'@{mention.user.screen_name} {list1[rand]}', mention.id)
            mention.favorite()
            mention.user.follow()
               

while True:
    reply_to_tweets()
    time.sleep(15)
