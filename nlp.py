import re
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger
from stemming.porter2 import stem
from nltk import bigrams
from action import Action
from decision import Decision
import stocksdata

stockTickers = [x.lower() for x in list(stocksdata.stocks.keys())]
stockTriggers = ["buy", "sell", "short", "fall", 'gain', 'rise']
stockTriggerWords = ["buy", "sell", "short", "fall", 'gain', 'rise', 'drop'] + [x.lower() for x in list(stocksdata.stocks.keys())]


ac = Action()
dec = Decision()


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

    user_input = message
    letters = re.sub("[^a-zA-Z0-9%]", " ", user_input)
    lower_letters = letters.lower()

    allwords = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    string = " ".join(str(x) for x in allwords)
    text = nltk.word_tokenize(string)
    pos = nltk.pos_tag(text)

    finalTerms = []
    print(pos)
    for i in pos:
        if i[0] in stockTriggerWords or i[1] == 'CD' or i[0] == '%':
            finalTerms.append(i)
    for i in finalTerms:
        if i[0] in stockTickers:
            tic = i[0]
        if i[1] == 'CD':
            amount = i[0]
        if i[0] == '%':
            amount += "%"
        if i[0] in stockTriggers:
            verb = i[0]
    if condition == "decision":
        dec.createDecision(tic, amount, verb)
    else:
        ac.createAction(tic, amount, verb)

splitString("If TSLA drops 5%, then I want to buy 20 shares of MSFT")
ac.print()
dec.print()