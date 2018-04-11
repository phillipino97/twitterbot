import tweepy
import time
import threading
import logging
from auth import *
from createtweets import *

#creates log for debugging. Saves private data, though
logfile = open("status.log", "w")
logfile.write("")
logfile.close()
logging.basicConfig(filename='status.log',level=logging.DEBUG)

#creates the authentication keys and then sets the api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
phillipsbot00 = api.get_user('phillipsbot00')
phillipino97 = api.get_user('phillipino97')
#opens analytics file with basic info
analytics = open("analytics.txt", "r")
analytics = analytics.read()
requested = analytics[analytics.find("requested {")+11:analytics.find("}")]
requested = requested.split("\n")
with open("followers.txt", "r") as myfile:
    followers_list = myfile.read()
    followers_list = followers_list.split("\n")
requested.remove("")
requested.remove("")
#holds all the thread instances
threads = []

#follows all people that my personal twitter follows
def follow_main():
    while True:
        for follower in tweepy.Cursor(api.friends, id="phillipino97").items():
            if follower.screen_name == 'phillipsbot00':
                pass
            else:
                try:
                    status = api.show_friendship(source_screen_name="phillipsbot00", target_screen_name=follower.screen_name)
                    if status[0].following != True:
                        follower.follow()
                        print "Followed " + follower.screen_name + "!"
                except:
                    for i in requested:
                        if i == follower.screen_name:
                            pass
        print "Following phillipino97 friends finished!"
        time.sleep(630)

def follow_followers():
    while True:
        for follower in tweepy.Cursor(api.followers, id="phillipsbot00").items():
            if follower.screen_name == 'phillipsbot00':
                pass
            else:
                try:
                    status = api.show_friendship(source_screen_name="phillipsbot00", target_screen_name=follower.screen_name)
                    if status[0].following != True:
                        follower.follow()
                        print "Followed " + follower.screen_name + "!"
                except:
                    for i in requested:
                        if i == follower.screen_name:
                            pass
        print "Following followers finished!"
        time.sleep(600)

def tweet_out():
    while True:
        to_sleep = random.randint(2700,16201)
        time.sleep(to_sleep)
        content = get_content_lyric()
        api.update_status(status=content)

def monitor_follows():
    followercnt = followers_list[len(followers_list)-1]
    while True:
        phillipsbot00 = api.get_user('phillipsbot00')
        if phillipsbot00.followers_count > followercnt:
            for i in range(phillipsbot00.followers_count - followercnt):
                print("Gained a new follower!")
            fol = tweepy.Cursor(api.followers, id="phillipsbot00").items()
            items = []
            for item in fol:
                items.append(item)
            send_message("Thanks for following!", items[len(items)-1])
            print_followers_to_file()
            followercnt = phillipsbot00.followers_count
        elif phillipsbot00.followers_count < followercnt:
            print("Lost a follower!")
            print_followers_to_file()
            followercnt = int(str(followers_list[len(followers_list)-1]))
        time.sleep(2)

def print_followers_to_file():
    with open("followers.txt", "w") as myfile:
        for follower in tweepy.Cursor(api.followers, id="phillipsbot00").items():
            myfile.write(follower.screen_name + "\n")
        phillipsbot00 = api.get_user('phillipsbot00')
        myfile.write(str(phillipsbot00.followers_count))
    followers_list = open("followers.txt", "r")
    followers_list = followers_list.read().split("\n")

def retweet_mentions():
    #creates the search query
    searchq = "@phillipsbot00-filter:retweets"
    #tweet limit so it doesn't time out
    tweetslimit = 100
    #opens up the list of retweeted tweets
    retweet_archive = open("retweet_ids.txt", "r")
    retweet_archive = retweet_archive.read()
    #opens up the list of favorited tweets
    favorite_archive = open("favorite_ids.txt", "r")
    favorite_archive = favorite_archive.read()
    while True:
        #searches for tweets with specified query
        new_tweets = api.search(q=searchq, count=tweetslimit)
        #the result of new_tweets is a list of all tweets with a mention of @phillipsbot00
        for i in new_tweets:
            #getting the tweet id from the tweet
            tweet_id = str(i)[str(i).find(", id=")+5:str(i).find("L, fav")]
            #creating a tweet instance that can tell us whether the tweet has been liked, retweeted, etc.
            tweet = api.get_status(tweet_id)
            #if the tweet has been liked or retweeted leave it alone and go on to the next one
            if tweet.retweeted or tweet.favorited:
                pass
            #if not, see what needs to be done with the tweet
            else:
                #creates a string instance of the tweet, I fucked up on the naming originally so I just added an extra s :P
                new_tweetss = str(i)
                #retrieves the username of the person who tweeted (insurance on the repeat after me function that we can keep track of who is using it)
                username = new_tweetss[new_tweetss.find("u\'screen_name\': u\'")+18:new_tweetss.find("\', u\'lang\':")]
                #if the case was no retweeted then it will check if it needs to be retweeted or repeated
                if not tweet.retweeted and "phillipsbot00" not in username:
                    #checks to see if it is a reply to a previous tweet, if it is it will move on to favoriting it (possibly move this back to a spot to increase productivity)
                    if "in_reply_to_status_id=None" in new_tweetss:

                        #if the tweet was a quoted tweet this will do something
                        if "is_quote_status=True" in new_tweetss:

                            pass
                        #checks to see if it needs to be repeated
                        if ", text=u\'@phillipsbot00 repeat after me:" in new_tweetss:
                            #if it is not favorited it will repeat it then favorite it
                            if not tweet.favorited:
                                #retrieves repeat text
                                text_to_repeat = new_tweetss[new_tweetss.find(", text=u\'@phillipsbot00 repeat after me:")+41:new_tweetss.find("\', is_qu")]
                                #checks if there are quotes and fixes them as formatting fucks it up
                                if "\u2018" in text_to_repeat:
                                    text_to_repeat = text_to_repeat.replace("\u2018", "\'")
                                    text_to_repeat = text_to_repeat.replace("\u2019", "\'")
                                #makes sure there is actually content to tweet
                                if len(text_to_repeat) > -1:
                                    #adds the repeated text and the username that sent it for insurance purposes
                                    with open("repeated.txt", "a") as myfile:
                                        myfile.write("\n" + text_to_repeat + " - " + username)
                                    #tweets
                                    api.update_status(status=text_to_repeat)
                                    #favorites
                                    api.create_favorite(tweet_id)
                                    print "Favorited and repeated " + tweet_id + "!"
                                    #adds the tweet id to the favorite_ids file for archiving
                                    with open("favorite_ids.txt", "a") as myfile:
                                        myfile.write("\n" + tweet_id)
                                pass
                        else:
                            #if it was not to be repeated then it will retweet
                             api.retweet(tweet_id)
                             print "Retweeted " + tweet_id + "!"
                             #adds the tweet id to the retweet_ids file for archiving
                             with open("retweet_ids.txt", "a") as myfile:
                                 myfile.write("\n" + tweet_id)
                    #if the tweet was retweeted it will go here
                    elif not tweet.favorited and "phillipsbot00" not in username:
                        #favorites
                        api.create_favorite(tweet_id)
                        print "Favorited " + tweet_id + "!"
                        #adds the tweet id to the favorite_ids file for archiving
                        with open("favorite_ids.txt", "a") as myfile:
                            myfile.write("\n" + tweet_id)
                else:
                    pass
                #buffer
                time.sleep(2)

def retweet_tweet(tweet_id):
    api.retweet(tweet_id)
    with open("tweet_ids.txt", "a") as myfile:
        myfile.write("\n" + tweet_id)

def send_message(message, usertomess):
    api.send_direct_message(usertomess.id, text=message)
    print "Messaged " + usertomess.screen_name + ": " + message

def start_threads(threadss):
    for thread in threadss:
        thread = threading.Thread(target=thread, args=())
        thread.start()
        threads.append(thread)

def main():
    try:
        print_followers_to_file()
        #send_message("hi", phillipino97)
        threadsto = [retweet_mentions, follow_main, follow_followers, tweet_out, monitor_follows]
        start_threads(threadsto)
    except Exception:
        logging.exception("Tweepy Error")
        logging.warning("Tweepy Error!")

if __name__== "__main__":
    logging.info("Program Startup")
    main()
