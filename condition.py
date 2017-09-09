class Condition:
    ticker = ""
    percentage = ""
    change = ""
    time = ""
    type = ""

    def __init__(self):
        pass

    def createCondition(self, ticker, percentage, change, time, type):
        self.ticker = ticker
        self.percentage = percentage
        self.change = change
        self.time = time
        self.type = type

    def print(self):
        cond = ""
        if type == True:
            cond = "Positive"
        else:
            cond = "Negative"
        print("CONDITION: " + self.ticker.upper() + " " + self.change + " by " + self.percentage + " from " + self.time + ". This is a " + cond + " change")
