class Action:
    ticker = ""
    amount = ""
    verb = ""
    def __init__(self):
        pass
    def createAction(self, ticker, amount, verb):
        self.ticker = ticker
        self.amount = amount
        self.verb = verb
    def print(self):
        print("ACTION: " + self.verb + " " + self.amount + " stocks of " + self.ticker.upper())