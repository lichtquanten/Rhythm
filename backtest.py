#!/usr/bin/env python

import zipline
from zipline.api import order, order_value, order_percent, record, symbol
import pandas as pd

def backtest(algo_config):
    def handle_data(context, data):
        asset_value = context.portfolio.cash
        for key in list(context.portfolio.positions):
            asset_value += context.portfolio.positions[key].amount*data.current(key, 'price');

        for algo in algo_config:
            should_act = False

            #CONDITION COMMAND CENTER
            payload = algo['condition']['payload']
            if algo['condition']['type'] == 'stocky':
                values = []
                for stock in payload['stocks']:
                    record(stock['ticker'], data.current(symbol(stock['ticker']), 'price'))
                    if stock['field'] == 'close_price':
                        previous_close_price = data.history(symbol(stock['ticker']), 'close', 2, '1d')[0]
                        values.append(previous_close_price)
                    else:
                        values.append(data.current(symbol(stock['ticker']), stock['field']))

                diff = values[0] - values[1]
                # print(str(diff))
                if payload['threshold_type'] == 'percent':
                    diff = diff/values[1]*100
                if payload['threshold'] > 0:
                    should_act = diff > payload['threshold']
                else:
                    should_act = diff < payload['threshold']

            #ACTION COMMAND CENTER
            if should_act:
                ticker_symbol = symbol(algo['action']['ticker'])
                target_change = algo['action']['amount']
                unit = algo['action']['amount_unit']
                current_amount = context.portfolio.positions[ticker_symbol].amount
                price = data.current(ticker_symbol, 'price')

                if algo['action']['position'] == 'long':
                    if target_change > 0: #long more
                        if current_amount < 0: #if currently shorting, get rid of short shares
                            order(current_amount)
                            asset_value += current_amount*price
                        if unit == 'dollars':
                            val = target_change if target_change < asset_value else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                        elif unit == 'shares':
                            val = target_change if target_change*price < asset_value else asset_value/price
                            order(ticker_symbol, val)
                            asset_value -= val*price
                        elif unit == 'percent_assets':
                            val = target_change*asset_value if target_change < 1 else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                        elif unit == 'percent_ownership':
                            val = current_amount*target_change*price if current_amount*target_change*price < asset_value else asset_value
                            order_value(ticker_symbol, val)
                            asset_value -= val
                    elif target_change < 0: #long less
                        if not current_amount < 0: #if currently shorting, longing less is meaningless
                            if unit == 'dollars':
                                val = target_change if abs(target_change) < current_amount*price else -current_amount*price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'shares':
                                val = target_change if abs(target_change) < current_amount else -current_amount
                                order(ticker_symbol, val)
                                asset_value += val*price
                            # not sure about this guy
                            elif unit == 'percent_assets':
                                val = target_change*asset_value if abs(target_change) < 1  and abs(target_change)*asset_value < current_amount*price else -current_amount*price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'percent_ownership':
                                val = current_amount*target_change*price if abs(target_change) < 1 and current_amount*abs(target_change)*price < asset_value else -current_amount*price
                                order_value(ticker_symbol, -val)
                                asset_value += val
                #shorting
                else:
                    if target_change > 0: #short more
                        if current_amount > 0: # if currently longing, sell long shares
                            order(-current_amount)
                            asset_value += current_amount*price
                        if asset_value > 0:
                            if unit == 'dollars':
                                val = target_change if target_change < asset_value else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                            elif unit == 'shares':
                                val = target_change if target_change*price < asset_value else asset_value/price
                                order(ticker_symbol, -val)
                                asset_value -= val*price
                            elif unit == 'percent_assets':
                                val = target_change*asset_value if target_change < 1 else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                            elif unit == 'percent_ownership':
                                val = current_amount*target_change*price if current_amount*target_change*price < asset_value else asset_value
                                order_value(ticker_symbol, -val)
                                asset_value -= val
                    elif target_change < 0: #short less
                        if not current_amount < 0: #if currently longing, shorting less is meaningless
                            if unit == 'dollars':
                                val = abs(target_change)/price if abs(target_change)/price < abs(current_amount) else abs(current_amount)
                                order(ticker_symbol, val)
                                asset_value += val*price
                            elif unit == 'shares':
                                val = abs(target_change) if abs(target_change) < abs(current_amount) else abs(current_amount)
                                order(ticker_symbol, val)
                                asset_value += val*price
                            elif unit == 'percent_assets':
                                val = abs(asset_value)*abs(target_change) if abs(target_change) < 1 and abs(asset_value)*abs(target_change) < abs(current_amount)*price else abs(current_amount)*price
                                order_value(ticker_symbol, val)
                                asset_value += val
                            elif unit == 'percent_ownership':
                                val = abs(current_amount)*abs(target_change) if abs(current_amount)*abs(target_change) < abs(current_amount) else abs(current_amount)
                                order(ticker_symbol, val)
                                asset_value += val



    zipline.run_algorithm(pd.Timestamp('2014-01-01', tz='utc'), pd.Timestamp('2014-11-01', tz='utc'), initialize, 100000, handle_data, analyze=analyze)

#used to define context
#context stores the portfolio object by default
def initialize(context):
    pass


def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    index = 211
    for key in list(results):
        if key == 'algo_volatility':
            break
        plt.figure()
        plt.suptitle(key)
        plt.plot(results[key])
        plt.xlabel('Time')
        plt.ylabel('Price of ' + key)

    plt.figure()
    plt.suptitle('Portfolio Value')
    plt.plot(results.portfolio_value)
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')

    plt.figure()
    plt.suptitle('Returns')
    plt.plot(results.returns)
    plt.xlabel('Time')
    plt.ylabel('Returns')

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
                'payload': {
                    'stocks': [
                        { 'ticker': 'AMZN', 'field': 'price' },
                        { 'ticker': 'AMZN', 'field': 'close_price' }
                    ],
                    'threshold': 1.2,
                    'threshold_type': 'percent'
                }
             }
        },
        {
            'action': {
                'ticker': 'AMZN',
                'amount': -.5,
                'amount_unit': 'percent',
                'position': 'long'
            },
            'condition': {
                'type': 'stocky',
                'payload': {
                    'stocks': [
                        { 'ticker': 'AMZN', 'field': 'price' },
                        { 'ticker': 'AMZN', 'field': 'close_price' }
                    ],
                    'threshold': -.5,
                    'threshold_type': 'percent'
                }
            }
        }
    ]
    backtest(demo_algo_config)
