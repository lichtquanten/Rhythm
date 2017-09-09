class Action:
    ticker = ""
    amount = ""
    verb = ""
    def __init__(self):
        pass
    def createAction(self, ticker, amount, verb):
        self.ticker = ticker

        if verb != "buy":
            self.amount = -1 * int(amount)
        else:
            self.amount = int(amount)
        self.verb = verb
    def print(self):
        print("ACTION: " + self.verb + " " + str(self.amount) + " stocks of " + self.ticker.upper())