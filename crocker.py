#!/usr/bin/env python3
"""
Plot Crocker Charts with average data if desired
Idea by Fred Goodman
"""
__author__ = "John Bolinger"
__version__ = "0.1.0"
__license__ = "MIT"
__copyright__ = "John Bolinger 2022"

# import necessary packages
import norgatedata
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import datetime

def Crocker():
    """ get the data and plot the chart """
    # get the data
    if norgate:
        df = norgatedata.price_timeseries(
            ticker,
            format='pandas-dataframe',
            stock_price_adjustment_setting = norgatedata.StockPriceAdjustmentType.TOTALRETURN,
            padding_setting = norgatedata.PaddingType.ALLMARKETDAYS,
            )
    else:
        start = datetime.datetime.now() - datetime.timedelta(days = 365)
        end = datetime.datetime.now()
        df = web.DataReader(ticker, 'yahoo', start=start, end=end)

    # select the data to plot
    if average: # calc averages
        avg_volume = df['Volume'].rolling(avg_len).mean()
        avg_price = df['Close'].rolling(avg_len).mean()
        volume = avg_volume.tail(plot_len)/1000
        price = avg_price.tail(plot_len)
    else:
        volume = df['Volume'].tail(plot_len)/1000
        price = df['Close'].tail(plot_len)

    # get some colors
    phi = np.linspace(0, 2*np.pi, plot_len)
    rgb_cycle = np.vstack((            # Three sinusoids
        .5*(1.+np.cos(phi          )), # scaled to [0,1]
        .5*(1.+np.cos(phi+2*np.pi/3)), # 120° phase shifted.
        .5*(1.+np.cos(phi-2*np.pi/3)))).T # Shape = (plot_lem,3)
    # labels
    plt.title(chartTitle + ' for ' + ticker)
    plt.xlabel("Volume")
    plt.ylabel("Price")
    # plot it
    plt.plot(volume, price)
    plt.scatter(volume, price, c=rgb_cycle)
    # plot a start andend dates
    plt.text(volume.values[:1], price.values[:1], price.index[0].date())
    plt.text(volume.values[-1], price.values[-1], price.index[-1].date())
    plt.show()
    if priceChart: # plot a price and volume chart
        fig, (a0, a1) = plt.subplots(nrows=2, ncols=1, \
                        sharex=True, gridspec_kw={'height_ratios':[2, 1]})
        #fig.tight_layout()
        a0.set_ylabel(ticker)
        x = df[-plot_len:].index.strftime('%d-%b')
        a0.plot(x, df['Close'][-plot_len:], color='blue', label=ticker)
        a1.bar(x, df['Volume'][-plot_len:]/1000, color='darkgrey')
        plt.xticks(np.arange(0, len(x), 5.0))
        plt.show()

if __name__ == "__main__":
    """ Entry point """
    # user controls
    norgate = True # Use Norgate data or else Yahoo!
    ticker = 'SPY' # the symbol to plot
    chartTitle = 'Crocker Chart'
    average = True # True to plot Crocker charts with averages
    avg_len = 5 # the moving avaerga elength is desired
    plot_len = 20 # how many periods to plot
    priceChart = True # True if you want to plot a price/volume chart
    # run the program
    Crocker()

# That's all folks!
