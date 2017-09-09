#!/usr/bin/env python

import zipline
from zipline.api import order, order_value, order_percent, record, symbol
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def backtest(algo_config):
    def handle_data(context, data):
        asset_value = context.portfolio.cash
        for key in list(context.portfolio.positions):
            asset_value += context.portfolio.positions[key].amount * data.current(key, 'price');

        for algo in algo_config:
            should_act = False

            # CONDITION COMMAND CENTER
            conditionals = algo['condition']['conditionals']
            if algo['condition']['type'] == 'stocky':

                for conditional in conditionals:
                    current_price = data.current(symbol(conditional['ticker']), 'price')
                    record(conditional['ticker'], current_price)
                    comparison_price = ""
                    if conditional['field'] == 'close_price':
                        comparison_price = data.history(symbol(conditional['ticker']), 'close', 2, '1d')[0]
                    elif conditional['field'] == 'open':
                        comparison_price = data.current(symbol(conditional['ticker']), 'open')

                    diff = ""
                    if conditional['threshold_type'] == 'percent':
                        diff = (current_price - comparison_price) / comparison_price * 100
                    else:
                        if conditional['threshold'] > 0:
                            diff = current_price - comparison_price
                        elif conditional['threshold'] < 0:
                            diff = comparison_price - current_price
                    if conditional['threshold'] > 0:
                        should_act = diff >= conditional['threshold']
                    else:
                        should_act = diff <= conditional['threshold']

                # ACTION COMMAND CENTER
            if should_act:
                ticker_symbol = symbol(algo['action']['ticker'])
                target_change = algo['action']['amount']
                unit = algo['action']['amount_unit']
                # current_share_count
                current_amount = context.portfolio.positions[ticker_symbol].amount
                price = data.current(ticker_symbol, 'price')

                # long function
                # clean up asset_value -= val
                if algo['action']['position'] == 'long':
                    if target_change > 0:  # long more
                        if current_amount < 0:  # if currently shorting, get rid of short shares
                            order(ticker_symbol, abs(current_amount))
                            asset_value += current_amount * price
                        if unit == 'dollars':
                            val = target_change if target_change < asset_value else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                        elif unit == 'shares':
                            val = target_change if target_change * price < asset_value else asset_value / price
                            order(ticker_symbol, val)
                            asset_value -= val * price
                        elif unit == 'percent_assets':
                            val = target_change * asset_value if target_change < 1 else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                        elif unit == 'percent_ownership':
                            val = current_amount * target_change * price if current_amount * target_change * price < asset_value else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                    elif target_change < 0:  # long less
                        if not current_amount < 0:  # if currently shorting, longing less is meaningless
                            if unit == 'dollars':
                                val = target_change if abs(
                                    target_change) < current_amount * price else -current_amount * price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'shares':
                                val = target_change if abs(target_change) < current_amount else -current_amount
                                order(ticker_symbol, val)
                                asset_value += val * price
                            # not sure about this guy
                            elif unit == 'percent_assets':
                                val = target_change * asset_value if abs(target_change) < 1 and abs(
                                    target_change) * asset_value < current_amount * price else -current_amount * price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'percent_ownership':
                                val = current_amount * target_change * price if abs(
                                    target_change) < 1 else -current_amount * price
                                order_value(ticker_symbol, val)
                                asset_value += val
                # shorting
                else:
                    if target_change > 0:  # short more
                        if current_amount > 0:  # if currently longing, sell long shares
                            order(-current_amount)
                            asset_value += current_amount * price
                        if asset_value > 0:
                            if unit == 'dollars':
                                val = target_change if target_change < asset_value else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                            elif unit == 'shares':
                                val = target_change if target_change * price < asset_value else asset_value / price
                                order(ticker_symbol, -val)
                                asset_value -= val * price
                            elif unit == 'percent_assets':
                                val = target_change * asset_value if target_change < 1 else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                            elif unit == 'percent_ownership':
                                val = current_amount * target_change * price if current_amount * target_change * price < asset_value else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                    elif target_change < 0:  # short less
                        # double check
                        if current_amount < 0:  # if currently longing, shorting less is meaningless
                            if unit == 'dollars':
                                val = abs(target_change) / price if abs(target_change) / price < abs(
                                    current_amount) else abs(current_amount)
                                order(ticker_symbol, val)
                                asset_value += val * price
                            elif unit == 'shares':
                                val = abs(target_change) if abs(target_change) < abs(current_amount) else abs(
                                    current_amount)
                                order(ticker_symbol, val)
                                asset_value += val * price
                            elif unit == 'percent_assets':
                                # why abs(target_change) < 1?
                                val = abs(asset_value) * abs(target_change) if abs(target_change) < 1 and abs(
                                    asset_value) * abs(target_change) < abs(current_amount) * price else abs(
                                    current_amount) * price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'percent_ownership':
                                val = abs(current_amount) * abs(target_change) if abs(target_change) < 1 else abs(
                                    current_amount)
                                order(ticker_symbol, val)
                                asset_value += val

    zipline.run_algorithm(pd.Timestamp('2014-01-01', tz='utc'), pd.Timestamp('2014-11-01', tz='utc'), initialize,
                          100000, handle_data, analyze=analyze)


# used to define context
# context stores the portfolio object by default
def initialize(context):
    pass


def analyze(context=None, results=None):
    for key in list(results):
        if key == 'algo_volatility':
            break
        plt.figure()
        plt.suptitle(key)
        plt.plot(results[key])
        plt.xlabel('Time')
        plt.ylabel('Price of ' + key)

    transactionPoints = results.loc[results['capital_used'] != 0]

    plt.figure()
    plt.suptitle('Portfolio Value vs Time')
    plt.plot(results.portfolio_value)
    plt.plot_date(transactionPoints.portfolio_value)
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.show()

    plt.figure()
    plt.suptitle('Stock Value vs Time')
    plt.plot(results.ending_value)
    plt.xlabel('Time')
    plt.ylabel('Stock Value')
    plt.show()

    plt.figure()
    plt.suptitle('Transactions vs Time')
    plt.plot(transactionPoints.portfolio_value)
    plt.xlabel('Time')
    plt.ylabel('Transaction Costs')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()


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
                'conditionals': [
                    {'ticker': 'AMZN', 'field': 'close_price', 'threshold': 3, 'threshold_type': 'percentage'},

                ]
            }
        }
    ]
    backtest(demo_algo_config)
