import re
import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem
from nltk import trigrams

stocks = {}

def getStocksData():
    file = open('stocksdata.txt', 'r')
    for i in file.readlines():
        stockData = i.split("|")
        stocks[stockData[0]] = stockData[1].split("-")[0][:-1]
    print(stocks)

getStocksData()

def analyzeString(message):
    user_input = message
    letters = re.sub("[^a-zA-Z0-9]", " ", user_input)
    lower_letters = letters.lower()
    words = [stem(w) for w in lower_letters.split() if not w in stopwords.words("english")]
    string = " ".join(str(x) for x in words)
    text = nltk.word_tokenize(string)
    print(nltk.pos_tag(text))
    for i in trigrams(words):
        print(i)


analyzeString("I want to buy 10 shares of AAPL if MSFT falls 5%")