import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_historical_data(ticker, start_date, end_date, interval='1d'):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

def calculate_ema(data, period=20):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    return ema

def calculate_cci(data, period=20):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    cci = (typical_price - typical_price.rolling(period).mean()) / (0.015 * typical_price.rolling(period).std())
    return cci

def calculate_bollinger_bands(data, period=20, num_std=2):
    sma = data['Close'].rolling(period).mean()
    std = data['Close'].rolling(period).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return upper_band, lower_band

def calculate_entry_points(data):
    data['EMA'] = calculate_ema(data)
    data['CCI'] = calculate_cci(data)
    data['UpperBand'], data['LowerBand'] = calculate_bollinger_bands(data)

    # 上位足のデータを取得し、1日足のindexにリサンプリング
    higher_timeframe_data = get_historical_data('SOXL', '2021-01-01', '2023-08-01', interval='5d')  # 上位足（例：週足）のデータを取得
    higher_timeframe_data = higher_timeframe_data.reindex(data.index, method='ffill')

    # 上位足のEMAを1日足のデータにリサンプリング
    higher_timeframe_ema = calculate_ema(higher_timeframe_data)

    # 上位足のEMAの傾きを計算
    higher_timeframe_ema_slope = higher_timeframe_ema.diff()
    print(higher_timeframe_ema_slope)

    for i in range(len(data)):
        if data['CCI'][i] <= -100 and data['Close'][i] <= data['LowerBand'][i] and higher_timeframe_ema_slope[i] >= -0.5:
            data.loc[data.index[i], 'Buy_Entry'] = True
        else:
            data.loc[data.index[i], 'Buy_Entry'] = False

    return data

def plot_entry_points(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.plot(data.index, data['UpperBand'], label='Upper Bollinger Band', color='blue', linestyle='--')
    plt.plot(data.index, data['LowerBand'], label='Lower Bollinger Band', color='red', linestyle='--')
    plt.fill_between(data.index, data['UpperBand'], data['LowerBand'], alpha=0.2)
    plt.scatter(data[data['Buy_Entry']].index, data[data['Buy_Entry']]['Close'], marker='^', color='green', label='Buy Entry')
    plt.legend()
    plt.title('Buy Entry Points')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

def main():
    ticker = 'SOXL'
    start_date = '2021-01-01'
    end_date = '2023-08-01'
    historical_data = get_historical_data(ticker, start_date, end_date)

    # エントリーポイントを計算
    entry_points_data = calculate_entry_points(historical_data)

    # エントリーポイントをプロット
    plot_entry_points(entry_points_data)

if __name__ == "__main__":
    main()