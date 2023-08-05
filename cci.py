import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt



expence_ratio = 0.0095

# データ取得
def get_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = 'SOXL'  # 例としてSOXLの株価を取得します
start_date = '2022-01-01'
end_date = '2023-08-01'
historical_data = get_historical_data(ticker, start_date, end_date)

#移動平均線の傾きを算出
def calculate_slope(data, period) :
    sma = data.rolling(period).mean()
    slope = (sma - sma.shift(period)) / period
    return slope
    

# CCIの計算
def calculate_cci(data, period=20):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    cci = (typical_price - typical_price.rolling(period).mean()) / (0.015 * typical_price.rolling(period).std())
    return cci


def calculate_entry_points(data, cci_period=20):
    data['CCI'] = calculate_cci(data, cci_period)
    data['ShortEntry'] = (data['CCI'] > 100) 
    data['LongEntry'] = (data['CCI'] < -100) 
    return data

def plot_entry_points(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.scatter(data[data['LongEntry']].index, data[data['LongEntry']]['Close'], marker='^', color='green', label='Long Entry')
    plt.scatter(data[data['ShortEntry']].index, data[data['ShortEntry']]['Close'], marker='v', color='red', label='Short Entry')
    plt.legend()
    plt.title('CCI - Entry Points')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

entry_points_data = calculate_entry_points(historical_data)
plot_entry_points(entry_points_data)