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
stockTimes = ['yesterday', 'close', 'purchas', 'bought', 'open']
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
        conditions = strings[0].split("and")
        for i in conditions:
            analyzeString(i, "condition")
        analyzeString(strings[1], "action")

    print(json.dumps({**con.toJSON(), **ac.toJSON()}))
    return [{**con.toJSON(), **ac.toJSON()}]


def analyzeString(message, condition):

    tic = ""
    amount = ""
    verb = ""
    amount_type = "shares"
    time = ""

    user_input = message
    letters = re.sub("[^a-zA-Z0-9%$@]", " ", user_input)
    lower_letters = letters.lower()

    allwords = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    string = " ".join(str(x) for x in allwords)
    text = nltk.word_tokenize(string)
    pos = nltk.pos_tag(text)
    finalTerms = []
    for i in pos:
        if i[0] in stockTriggers+stockTickers+stockSymbols or i[1] == 'CD':
            finalTerms.append(i)
    print(finalTerms)
    for i in finalTerms:
        if i[0] in stockTickers and i[1] != "VB":
            tic = i[0]
        elif i[1] == 'CD':
            amount += i[0]
        elif i[0] == '%':
            amount_type = "percent"
        elif i[0] == '$':
            amount_type = "dollars"
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
    if condition == "condition":

        con.createCondition(tic, amount, amount_type, verb, time, type)
    else:
        ac.createAction(tic, amount, amount_type, verb)

