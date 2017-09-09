class Condition:
    ticker = ""
    amount = ""
    verb = ""
    time = ""
    cond = ""
    amount_type = ""
    is_percentage = ""

    def __init__(self):
        pass

    def createCondition(self, ticker, amount, amount_type, verb, time, type):
        self.ticker = ticker

        self.verb = verb
        self.amount_type = amount_type
        if type == True:
            self.amount = int(amount)
        else:
            self.amount = -1 * int(amount)
        if time == "yesterday" or time == "close":
            self.time = "price"
        else:
            self.time = "close_price"

    def print(self):
        print("CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change")

    def toString(self):
        return "CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change"

    def toJSON(self):
        return {"condition":{'type': 'stocky', 'payload':{'stocks':[{"ticker": self.ticker.upper(), "field":self.time}], 'threshold': self.amount, 'threshold_type':self.amount_type}}}
""" 
'condition': {
        'type': 'stocky',
        'payload': {
            'stocks': [
                {'ticker': 'MSFT', 'field': 'price'},
                {'ticker': 'MSFT', 'field': 'close_price'}
            ],
            'threshold': -10,
            'threshold_type': 'percent'
        }
    }
"""
