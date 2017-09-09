class Condition:
    ticker = ""
    percentage = ""
    change = ""
    time = ""

    def __init__(self):
        pass

    def createCondition(self, ticker, percentage, change, time):
        self.ticker = ticker
        self.percentage = percentage
        self.change = change
        self.time = time

    def print(self):
        print("CONDITION: " + self.ticker.upper() + " " + self.change + " by " + self.percentage + " from " + self.time)
