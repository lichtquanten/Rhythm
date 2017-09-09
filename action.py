class Action:
    ticker = ""
    amount = ""
    verb = ""
    amount_unit = ""

    def __init__(self):
        pass

    def createAction(self, ticker, amount, amount_unit, verb):
        self.ticker = ticker
        self.amount_unit = amount_unit
        if verb != "buy":
            self.amount = -1 * int(amount)
            self.verb = "short"
        else:
            self.amount = int(amount)
            self.verb = "long"

    def print(self):
        print("ACTION: " + self.verb + " " + str(self.amount) + " stocks of " + self.ticker.upper())

    def toString(self):
        return "ACTION: " + self.verb + " " + str(self.amount) + " stocks of " + self.ticker.upper()

    def toJSON(self):
        return {"action":{"ticker":self.ticker.upper(), "amount":int(self.amount), "amount_unit": self.amount_unit, "position":self.verb.lower()}}
"""
    'action': {
        'ticker': 'MSFT',
        'amount': 200,
        'amount_unit': 'dollars',
        'position': 'short'
    },

"""