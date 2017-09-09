class Decision:
    ticker = ""
    percentage = ""
    change = ""
    def __init__(self):
        pass
    def createDecision(self, ticker, percentage, change):
        self.ticker = ticker
        self.percentage = percentage
        self.change = change
    def print(self):
        print("DECISION: " + self.ticker.upper() + " " + self.change + " by " + self.percentage)
