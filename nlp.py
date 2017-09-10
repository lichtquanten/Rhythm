import re
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
from action import Action
from condition import Condition
import stocksdata
import json

stockTickers = [x.lower() for x in list(stocksdata.stocks.keys())]
stockTimes = ['yesterday', 'close', 'purchas', 'bought', 'open', 'move']
stockDecisionsPositive = ['gain', 'rise', 'up', 'win']
stockDecisionsNegative = ['fall', 'drop', 'lose', 'down']
stockActions = ["buy", "sell", "short"]
stockSymbols = ["$", "%"]
stockTriggers = stockTimes + stockDecisionsPositive + stockDecisionsNegative + stockActions

ac = Action()
con = Condition()

def splitString(message):
    message = message.lower()
    m = message.split(". ")
    if len(m) > 1:
        for i in m:
            splitString(i)
    #print(message)
    if len(message) > 1 and (message.index("if") == 0 or message.index("if") == 1):
        strings = message.split(",")
        conditions = strings[0].split(" ")
        cond = ""
        for word in conditions:
            if word == "and":
                analyzeString(cond, "condition", "and")
                cond = ""
            elif word == "or":
                analyzeString(cond, "condition", "or")
                cond = ""
            else:
                cond += word + " "
        analyzeString(cond, "condition", "na")
        analyzeString(strings[1], "action", "na")

    #print(json.dumps({**con.toJSON(), **ac.toJSON()}))
    return [{**con.toJSON(), **ac.toJSON()}]


def analyzeString(message, condition, conjunction):

    tic = ""
    amount = 0
    verb = ""
    amount_type = "shares"
    time = ""
    type = ""
    user_input = message
    letters = re.sub("[^a-zA-Z0-9%$@]", " ", user_input)
    lower_letters = letters.lower()

    allwords = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    string = " ".join(str(x) for x in allwords)
    text = nltk.word_tokenize(string)
    pos = nltk.pos_tag(text)
    finalTerms = []
    for i in pos:
        if i[0] in stockTriggers+stockTickers+stockSymbols+['day', 'earnings'] or i[1] == 'CD':
            finalTerms.append(i)
    for i in range(len(finalTerms)):
        val = finalTerms[i][0]
        if val in stockTickers and finalTerms[i][1] != "VB":
            tic = val
        elif finalTerms[i][1] == 'CD':
            if finalTerms[i+1][0] == 'day':
                sma_days = val
            else:
                amount += float(val)
        elif val == '%':
            amount_type = "percent"
        elif val == '$':
            amount_type = "dollars"
        elif val in stockDecisionsPositive:
            verb = val
            type = True
        elif val in stockDecisionsNegative:
            verb = val
            type = False
        elif val in stockActions:
            verb = val
        # elif val in ['earnings', 'profit']
        elif val in stockTimes:
            if val == "purchas":
                time = "purchase"
            elif val == "move":
                time = "sma"
            else:
                time = val
    if condition == "condition":
        if time == 'sma':
            time = 'sma' + str(sma_days)
        con.createCondition(tic, amount, amount_type, verb, time, type, conjunction)
    else:
        ac.createAction(tic, amount, amount_type, verb)

#print(splitString("If MSFT falls $3 from yesterday, buy 10 stocks of AAPL. If MSFT rises $5 from close, buy 5 stocks of AAPL."))
