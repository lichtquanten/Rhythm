#!/usr/bin/env python
#
# Copyright 2014 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import zipline

from zipline.api import order, record, symbol
import pandas as pd

def backtest(algo):
    def handle_data(context, data):
        should_act = False

        payload = algo['condition']['payload']
        if algo['condition']['type'] == 'stocky':
            stock_values = []
            for stock in payload['stocks']:
                # print(data.current(symbol(stock['ticker']), 'price'))
                record(stock['ticker'], data.current(symbol(stock['ticker']), 'price'))
                if stock['field'] == 'close_price':
                    previous_close_price = data.history(symbol(stock['ticker']), 'close', 2, '1d')[0]
                    stock_values.append(previous_close_price)
                else:
                    stock_values.append(data.current(symbol(stock['ticker']), stock['field']))
            if payload['comparison'] == '>' or payload['comparison'] == '<':
                diff = stock_values[0] - stock_values[1]
                if payload['magnitude_type'] == 'percent':
                    diff = diff/stock_values[1]*100
                if payload['comparison'] == '>':
                    should_act = diff > payload['magnitude']
                else:
                    should_act = diff < payload['magnitude']
        if should_act and data.current(symbol(algo['action']['ticker']), 'price') < context.portfolio.cash:
            print("CASH:" + str(context.portfolio.cash))
            print("COST:" + str(data.current(symbol(algo['action']['ticker']), 'price')))
            order(symbol(algo['action']['ticker']), algo['action']['amount'])
    zipline.run_algorithm(pd.Timestamp('2014-01-01', tz='utc'), pd.Timestamp('2014-11-01', tz='utc'), initialize, 500, handle_data, analyze=analyze)

#used to define context
#context stores the portfolio object by default
def initialize(context):data.current(symbol(algo['action']['ticker'])
    pass


def analyze(context=None, results=None):
    print("STA", results.ending_cash)
    print(list(results))
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.ending_cash.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.MSFT.plot(ax=ax2)
    ax2.set_ylabel('MSFT price (USD)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()

if __name__ == "__main__":
    demoAlgo = {
        'action': {
            'ticker': 'MSFT',
            'amount': 500,
            'amount_unit': 'shares',
            'position': 'long'
        },
        'condition': {
            'type': 'stocky',
            'payload': {
                'stocks': [
                    { 'ticker': 'MSFT', 'field': 'price' },
                    { 'ticker': 'MSFT', 'field': 'close_price' }
                ],
                'comparison': '>',
                'magnitude': .5,
                'magnitude_type': 'percent'
            }
        }
    }
    backtest(demoAlgo)

