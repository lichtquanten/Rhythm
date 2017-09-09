class Condition:
    ticker = ""
    amount = ""
    verb = ""
    time = ""
    cond = ""
    person = ""
    is_percentage = ""
    is_twitter = ""
    def __init__(self):
        pass

    def createCondition(self, ticker, amount, verb, time, type, person, is_twitter):
        self.ticker = ticker
        self.amount = amount
        self.verb = verb
        self.time = time
        self.person = person

        if type == True:
            self.cond = "positive"
        else:
            self.cond = "negative"
        self.type = type

        if is_twitter == True:
            self.is_twitter = True
            self.is_percentage = False
        else:
            if amount[-1:] == "%":
                self.is_percentage = True
            else:
                self.is_percentage = False
            self.is_twitter = False

    def print(self):
        print("CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change")

    def toString(self):
        return "CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change"

    def toJSON(self):
        return {"condition":{"ticker": self.ticker.upper(), "amount": self.amount, "verb": self.cond, "time":self.time, "is_percentage": self.is_percentage, "is_twitter": self.is_twitter, "person": self.person}}