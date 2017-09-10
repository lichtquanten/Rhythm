#!/usr/bin/env python
import zipline
from zipline.api import order, order_value, order_percent, record, symbol
from datetime import datetime
from threading import Timer
import pandas as pd
import quandl
quandl.ApiConfig.api_key = "DEFAULT_KEY"
from InvestopediaApi import ita
client = ita.Account("default@email.com", "default password")
import nlp



def refresh():
    buying_power = ita.Account.get_portfolio_status['buying_power']

    for algo in algos:
        if shouldAct(algo['condition']['logic']):
            ticker = algo['action']['ticker']
            target_change = algo['action']['amount']
            unit = algo['action']['amount_unit']
            # current_share_count

            current_quantity = client.get_current_securities[ticker].quanity
            price = ita.get_quote(ticker)

            long = algo['action']['position'] == 'long'
            if target_change > 0:
                if long:
                    if current_amount < 0:
                        client.trade(ticker_symbol, abs(current_amount))
                        buying_power += abs(current_amount) * price
                else:
                    if current_amount > 0:  # if currently longing, sell long shares
                        client.trade(-current_amount)
                        buying_power += current_amount * price
                if buying_power > 0:
                    if unit == 'dollars':
                        val = target_change / price if target_change < buying_power else buying_power / price
                    elif unit == 'shares':
                        val = target_change if target_change * price < buying_power else buying_power / price
                    elif unit == 'percent_assets':
                        val = target_change * buying_power / price if target_change < 1 else buying_power / price
                    elif unit == 'percent_ownership':
                        val = abs(current_amount) * target_change if abs(current_amount) * target_change * price < buying_power else buying_power / price
                    client.trade(ticker_symbol, val if long else -val)
                    buying_power -= val * price
            else:
                if (long and current_amount > 0) or (not long and current_amount < 0):
                    if unit == 'dollars':
                        val = target_change / price if abs(target_change) / price < abs(current_amount) else -abs(current_amount)
                    elif unit == 'shares':
                        val = target_change if abs(target_change) < abs(current_amount) else -abs(current_amount)
                    elif unit == 'percent_assets':
                        val = 0
                        if buying_power > 0:
                            val = target_change * buying_power / price if target_change > -1 and buying_power * abs(target_change) < abs(current_amount) * price else -abs(current_amount)
                    elif unit == 'percent_ownership':
                        val = abs(current_amount) * target_change if target_change > -1 else -abs(current_amount)
                    client.trade(ticker_symbol, val if long else -val)
                    buying_power -= val * price

def shouldAct(conditions):
    for i in range(0, len(logic), 2):
        condition_truth = test_condition(conditions[i])
        if len(logic) - 1 > i:
            if logic[i + 1] == 'or':
                if conditional_truth:
                    return True
                else:
                    continue
            elif logic[i + 1] == 'and':
                if conditional_truth:
                    continue
                else:
                    return False
        else:
            return conditional_truth

def test_condition(condition):
    ticker = condition['ticker']
    field = condition['field']
    current_price = ita.get_quote(ticker)

    if field == 'close_price':
        comparison_price = client.history(ticker, 'close', 2, '1d')[0]
    elif conditional['field'] == 'open':
        comparison_price = client.history(ticket, 'open', 1, '1d')[0]
    elif conditional['field'][:3] == 'sma':
        comparison_price = sum(client.history(ticker, 'close', int(conditional['field'][3:]), '1d'))/int(conditional['field'][3:])
    diff = (current_price - comparison_price) / (comparison_price * 100 if conditional['threshold_type'] == 'percent' else 1)

    return (conditional['threshold'] > 0 and diff > 0 or conditional['threshold'] < 0 and diff < 0) and (abs(diff) > abs(conditional['threshold']))

if __name__ == "__main__":
    while 1:
        x=datetime.today()
        wait_time = x.replace(day=x.day+1, hour=12, minute=0, second=0, microsecond=0) - x
        t = Timer(wait_time.seconds + 1, refresh)
        t.start()
algos = [{'condition': {'type': 'stocky', 'logic': [{'field': 'close_price', 'threshold': 0.02, 'ticker': 'AMZN', 'threshold_type': 'percentage'}, 'or', {'field': 'open', 'threshold': 500, 'ticker': 'AMZN', 'threshold_type': 'dollars'}]}, 'action': {'amount_unit': 'shares', 'position': 'long', 'ticker': 'AMZN', 'amount': 2}}]
