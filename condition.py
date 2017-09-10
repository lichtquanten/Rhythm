class Condition:
    ticker = ""
    amount = ""
    verb = ""
    time = ""
    cond = ""
    amount_type = ""
    is_percentage = ""

    conditions = []

    def __init__(self):
        pass

    def createCondition(self, ticker, amount, amount_type, verb, time, type, conjunction):
        self.ticker = ticker

        self.verb = verb
        self.amount_type = amount_type
        if type == True:
            self.amount = int(amount)
        else:
            self.amount = -1 * int(amount)
        if time == "yesterday" or time == "close":
            self.time = "close_price"
        elif time == "open":
            self.time = "open"
        self.conditions.append({"ticker": self.ticker.upper(), "field":self.time, 'threshold': self.amount, 'threshold_type':self.amount_type})
        if conjunction != "na":
            self.conditions.append(conjunction)

    def print(self):
        print("CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change")

    def toString(self):
        return "CONDITION: " + self.ticker.upper() + " " + self.verb + " by " + self.amount + " from " + self.time + ". This is a " + self.cond + " change"

    def toJSON(self):
        print(self.conditions)
        return {"condition":{'type': 'stocky', 'logic':self.conditions}}
""" 
'condition': {
        'type': 'stocky',
        'payload': {
            'stocks': [
                {'ticker': 'MSFT', 'field': 'price', 'threshold': -10,'threshold_type': 'percent'},
                {'ticker': 'AMZN', 'field': 'close_price'}
            ],
            'threshold': -10,
            'threshold_type': 'percent'
        }
    }
"""
