
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt



expence_ratio = 0.0095

# データ取得
def get_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = 'SOXL'  # 例としてApple社の株価を取得します
start_date = '2022-01-01'
end_date = '2023-08-01'
historical_data = get_historical_data(ticker, start_date, end_date)

# CCIの計算
def calculate_cci(data, period=50):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    cci = (typical_price - typical_price.rolling(period).mean()) / (0.015 * typical_price.rolling(period).std())
    return cci

# ボリンジャーバンドの計算
def calculate_bollinger_bands(data, period=50, num_std=2):
    sma = data['Close'].rolling(period).mean()
    std = data['Close'].rolling(period).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return upper_band, lower_band

def calculate_entry_points(data, cci_period=50, bb_period=50, bb_num_std=2):
    data['CCI'] = calculate_cci(data, cci_period)
    data['UpperBand'], data['LowerBand'] = calculate_bollinger_bands(data, bb_period, bb_num_std)
    data['ShortEntry'] = (data['CCI'] > 100) & (data['Close'] > data['UpperBand'])
    data['LongEntry'] = (data['CCI'] < -100) & (data['Close'] < data['LowerBand'])
    return data

def plot_entry_points(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.plot(data.index, data['UpperBand'], label='Upper Bollinger Band', color='blue', linestyle='--')
    plt.plot(data.index, data['LowerBand'], label='Lower Bollinger Band', color='red', linestyle='--')
    plt.fill_between(data.index, data['UpperBand'], data['LowerBand'], alpha=0.2)
    plt.scatter(data[data['LongEntry']].index, data[data['LongEntry']]['Close'], marker='^', color='green', label='Long Entry')
    plt.scatter(data[data['ShortEntry']].index, data[data['ShortEntry']]['Close'], marker='v', color='red', label='Short Entry')
    plt.legend()
    plt.title('CCI and Bollinger Bands - Entry Points')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

entry_points_data = calculate_entry_points(historical_data)
plot_entry_points(entry_points_data)