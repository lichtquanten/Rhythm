#!/usr/bin/env python

import zipline
from zipline.api import order, order_value, order_percent, record, symbol
import pandas as pd
import matplotlib.pyplot as plt
import nlp
import pprint
import seaborn as sns

def backtest(algo_config):
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(algo_config)

    def handle_data(context, data):
        asset_value = context.portfolio.cash
        for key in list(context.portfolio.positions):
            asset_value += context.portfolio.positions[key].amount * data.current(key, 'price');

        for algo in algo_config:
            should_act = False

            # CONDITION COMMAND CENTER
            logic = algo['condition']['logic']
            for i in range(0, len(logic), 2):
                conditional_truth = test_conditional(logic[i], context, data)
                if len(logic) - 1 > i:
                    if logic[i + 1] == 'or':
                        if conditional_truth:
                            should_act = True
                            break
                        else:
                            continue
                    elif logic[i + 1] == 'and':
                        if conditional_truth:
                            continue
                        else:
                            should_act = False
                            break
                else:
                    should_act = False
                    break



            # ACTION COMMAND CENTER
            if should_act:
                ticker = algo['action']['ticker']
                ticker_symbol = symbol(ticker)
                target_change = algo['action']['amount']
                unit = algo['action']['amount_unit']
                # current_share_count
                current_amount = context.portfolio.positions[ticker_symbol].amount
                price = data.current(ticker_symbol, 'price')

                long = algo['action']['position'] == 'long'
                if target_change > 0:
                    if long:
                        if current_amount < 0:  # if currently shorting, get rid of short shares
                            order(ticker_symbol, abs(current_amount))
                            asset_value += abs(current_amount) * price
                    else:
                        if current_amount > 0:  # if currently longing, sell long shares
                            order(-current_amount)
                            asset_value += current_amount * price
                    if asset_value > 0:
                        if unit == 'dollars':
                            val = target_change / price if target_change < asset_value else asset_value / price
                        elif unit == 'shares':
                            val = target_change if target_change * price < asset_value else asset_value / price
                        elif unit == 'percent_assets':
                            val = target_change * asset_value / price if target_change < 1 else asset_value / price
                        elif unit == 'percent_ownership':
                            val = abs(current_amount) * target_change if abs(current_amount) * target_change * price < asset_value else asset_value / price
                        order(ticker_symbol, val if long else -val)
                        asset_value -= val * price
                else:
                    if (long and current_amount > 0) or (not long and current_amount < 0):
                        if unit == 'dollars':
                            val = target_change / price if abs(target_change) / price < abs(current_amount) else -abs(current_amount)
                        elif unit == 'shares':
                            val = target_change if abs(target_change) < abs(current_amount) else -abs(current_amount)
                        elif unit == 'percent_assets':
                            val = 0
                            if asset_value > 0:
                                val = target_change * asset_value / price if target_change > -1 and asset_value * abs(target_change) < abs(current_amount) * price else -abs(current_amount)
                        elif unit == 'percent_ownership':
                            val = abs(current_amount) * target_change if target_change > -1 else -abs(current_amount)
                        order(ticker_symbol, val if long else -val)
                        asset_value -= val * price

    zipline.run_algorithm(pd.Timestamp('2014-01-01', tz='utc'), pd.Timestamp('2014-11-01', tz='utc'), initialize,
                          1000, handle_data, analyze=analyze, data_frequency='daily')


# used to define context
# context stores the portfolio object by default
def initialize(context):
    pass


def analyze(context=None, results=None):
    final_pnl = context.portfolio.pnl
    for key in list(results):
        if key == 'algo_volatility':
            break
        plt.figure()
        plt.suptitle(key)
        plt.plot(results[key])
        plt.xlabel('Time')
        plt.ylabel('Price of ' + key)

    transactionPoints = results.loc[results['capital_used'] != 0]
    transactionPoints = transactionPoints.reset_index()

    plt.figure()
    plt.suptitle('Portfolio Value vs Time')
    plt.plot(results.portfolio_value)
    plt.plot_date(transactionPoints['index'], transactionPoints['portfolio_value'])
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.savefig('portfolio_value.png')

    plt.figure()
    plt.suptitle('Stock Value vs Time')
    plt.plot(results.ending_value)
    plt.xlabel('Time')
    plt.ylabel('Stock Value')
    plt.savefig('stock_value.png')

    plt.figure()
    plt.suptitle('Transactions vs Time')
    plt.plot(transactionPoints.portfolio_value)
    plt.xlabel('Time')
    plt.ylabel('Transaction Costs')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.savefig('transactions.png')


def test_conditional(conditional, context, data):
    meme = 'sma14'
    print("YO" + str(sum(data.history(symbol(conditional['ticker']), 'close', int(meme[3:]), '1d')/int(meme[3:]))))

    current_price = data.current(symbol(conditional['ticker']), 'price')
    record(conditional['ticker'], current_price)
    if conditional['field'] == 'close_price':
        comparison_price = data.history(symbol(conditional['ticker']), 'close', 2, '1d')[0]
    elif conditional['field'] == 'open':
        comparison_price = data.current(symbol(conditional['ticker']), 'open')
    elif conditional['field'][:3] == 'sma':
        comparison_price = sum(data.history(symbol(conditional['ticker']), 'close', int(conditional['field'][3:]), '1d'))/int(conditional['field'][3:])
    diff = (current_price - comparison_price) / (comparison_price * 100 if conditional['threshold_type'] == 'percent' else 1)

    if conditional['field'] == 'earnings':
        diff = context.porfolio.pnl
    return (conditional['threshold'] > 0 and diff > 0 or conditional['threshold'] < 0 and diff < 0) and (
        abs(diff) > abs(conditional['threshold']))


if __name__ == "__main__":
    demo_algo_config = [
        {
            'action': {
                'ticker': 'AMZN',
                'amount': 2,
                'amount_unit': 'shares',
                'position': 'long'
            },
            'condition': {
                'type': 'stocky',
                'logic': [
                    {'ticker': 'AMZN', 'field': 'close_price', 'threshold': 0.02, 'threshold_type': 'percentage'},
                    'or',
                    {'ticker': 'AMZN', 'field': 'open', 'threshold': 500, 'threshold_type': 'dollars'}
                ]
            }
        }]


    backtest(nlp.splitString("If AMZN rises by 0.02% from close or if AMZN rises $500 from open, then buy 2 shares of AMZN"))
