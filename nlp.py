import re
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
from action import Action
from condition import Condition
import stocksdata

stockTickers = [x.lower() for x in list(stocksdata.stocks.keys())]
stockTimes = ['yesterday', 'purchas', 'bought']
stockDecisionsPositive = ['gain', 'rise', 'up', 'win']
stockDecisionsNegative = ['fall', 'drop', 'lose', 'down']
stockActions = ["buy", "sell", "short"]
stockTriggers = stockTimes + stockDecisionsPositive + stockDecisionsNegative + stockActions


ac = Action()
con = Condition()


def splitString(message):
    message = message.lower()
    if message.index("if") == 0:
        strings = message.split(",")
        analyzeString(strings[0], "decision")
        analyzeString(strings[1], "action")

def analyzeString(message, condition):

    tic = ""
    amount = ""
    verb = ""
    time = ""
    positive = False

    user_input = message
    letters = re.sub("[^a-zA-Z0-9%$]", " ", user_input)
    lower_letters = letters.lower()

    allwords = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    string = " ".join(str(x) for x in allwords)
    text = nltk.word_tokenize(string)
    pos = nltk.pos_tag(text)

    finalTerms = []
    for i in pos:
        if i[0] in stockTriggers+stockTickers or i[1] == 'CD' or i[0] == '%' or i[0] == "$":
            finalTerms.append(i)
    for i in finalTerms:
        print(i)
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
        con.createCondition(tic, amount, verb, time, type)
    else:
        ac.createAction(tic, amount, verb)

splitString("If TSLA drops $5 from purchase price, then I want to buy 20 shares of MSFT")
ac.print()
con.print()