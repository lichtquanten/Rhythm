class Condition:
    ticker = ""
    percentage = ""
    change = ""
    time = ""
    type = ""
    is_percentage = ""
    def __init__(self):
        pass

    def createCondition(self, ticker, percentage, change, time, type):
        self.ticker = ticker
        self.percentage = percentage
        self.change = change
        self.time = time
        self.type = type

        if percentage[-1:] == "%":
            is_percentage = True
        else:
            is_percentage = False

    def print(self):
        cond = ""
        if type == True:
            cond = "Positive"
        else:
            cond = "Negative"
        print("CONDITION: " + self.ticker.upper() + " " + self.change + " by " + self.percentage + " from " + self.time + ". This is a " + cond + " change")

    def toString(self):
        cond = ""
        if type == True:
            cond = "Positive"
        else:
            cond = "Negative"
        return "CONDITION: " + self.ticker.upper() + " " + self.change + " by " + self.percentage + " from " + self.time + ". This is a " + cond + " change"
