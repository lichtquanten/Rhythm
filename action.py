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
            self.verb = "negative"
        else:
            self.amount = int(amount)
            self.verb = "positive"

    def print(self):
        print("ACTION: " + self.verb + " " + str(self.amount) + " stocks of " + self.ticker.upper())

    def toString(self):
        return "ACTION: " + self.verb + " " + str(self.amount) + " stocks of " + self.ticker.upper()

    def toJSON(self):
        return {"action":{"ticker":self.ticker.upper(), "amount":str(self.amount), "action":self.verb}}