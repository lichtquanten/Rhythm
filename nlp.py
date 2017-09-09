import re
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
from action import Action
from condition import Condition
import stocksdata
import json
import tweepy

stockTickers = [x.lower() for x in list(stocksdata.stocks.keys())]
stockTimes = ['yesterday', 'purchas', 'bought']
stockDecisionsPositive = ['gain', 'rise', 'up', 'win']
stockDecisionsNegative = ['fall', 'drop', 'lose', 'down']
stockActions = ["buy", "sell", "short"]
stockSymbols = ["$", "%"]
stockTriggers = stockTimes + stockDecisionsPositive + stockDecisionsNegative + stockActions

ac = Action()
con = Condition()

def splitString(message):
    message = message.lower()
    if message.index("if") == 0:
        strings = message.split(",")
        analyzeString(strings[0], "decision")
        analyzeString(strings[1], "action")

    return json.dumps({**ac.toJSON(), **con.toJSON()})


def analyzeString(message, condition):

    tic = ""
    amount = ""
    verb = ""
    time = ""
    twitter_person = ""
    is_twitter = False

    user_input = message
    letters = re.sub("[^a-zA-Z0-9%$@]", " ", user_input)
    lower_letters = letters.lower()

    allwords = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    print(allwords)
    for i in allwords:
        if i[:1] == "@":
            twitter_person = i
            is_twitter = True
    string = " ".join(str(x) for x in allwords)
    text = nltk.word_tokenize(string)
    pos = nltk.pos_tag(text)
    finalTerms = []
    for i in pos:
        if i[0] in stockTriggers+stockTickers+stockSymbols or i[1] == 'CD':
            finalTerms.append(i)
    for i in finalTerms:
        if i[0] in stockTickers:
            tic = i[0]
        elif i[1] == 'CD':
            amount += i[0]
        elif i[0] == '%':
            amount += "%"
        elif i[0] == '$':
            amount += "$"
        elif i[0] in stockDecisionsPositive:
            verb = i[0]
            type = True
        elif i[0] in stockDecisionsNegative:
            verb = i[0]
            type = False
        elif i[0] in stockActions:
            verb = i[0]
        elif i[0] in stockTimes:
            if i[0] == "purchas":
                time = "purchase"
            else:
                time = i[0]
    if condition == "decision":

        con.createCondition(tic, amount, verb, time, type, twitter_person, is_twitter)
    else:
        ac.createAction(tic, amount, verb)

print(splitString("If @realDonaldTrump tweets about stocks dropping, short 10 shares of that stock "))
print(splitString("If MSFT falls by 5% from yesterday, buy 10 AAPL Shares"))