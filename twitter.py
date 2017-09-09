import tweepy
import stocksdata

stockTickers = [x for x in list(stocksdata.stocks.keys())]

consumer_key = "E6e9gKPhRRZKqQqgD6BileWaw"
consumer_secret = "k3XybwbUR0jUa6myFRRjfkp75GnTtp30ZiZ07RQ2SD4WN3cXcH"
access_key = "875092091407261697-KV5fM4CS5pHKl7TyJZQmfLHNZjLypzB"
access_secret = "q7eTyqrWwcMqOFlujc9X2w74tEWUAaS4vJJJz5OGnXp7S"

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    stockTweets = []
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and len(alltweets) < 2000:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    for i in alltweets:
        for word in i.text.split(" "):
            if word.lower() == "nasdaq":
                stockTweets.append(i.text)
    for i in stockTweets:
        print(i)

get_all_tweets("@realDonaldTrump")