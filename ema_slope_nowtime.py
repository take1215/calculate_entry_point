import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_ema_slope(data, period=20):
    ema = data['Close'].ewm(span=period, adjust=False).mean()
    ema_slope = ema.diff()
    return ema_slope

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

def calculate_entry_points(data, ema_period=20, cci_period=20, bb_period=20, bb_num_std=2):
    data['EMA_Slope'] = calculate_ema_slope(data, ema_period)
    data['CCI'] = calculate_cci(data, cci_period)
    data['UpperBand'], data['LowerBand'] = calculate_bollinger_bands(data, bb_period, bb_num_std)

    # 買いのエントリーポイントを算出
    data['Buy_Entry'] = (data['EMA_Slope'] > -1.0) & (data['CCI'] <= -100) & (data['Close'] <= data['LowerBand'])
    
    return data

def plot_entry_points(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.plot(data.index, data['UpperBand'], label='Upper Bollinger Band', color='blue', linestyle='--')
    plt.plot(data.index, data['LowerBand'], label='Lower Bollinger Band', color='red', linestyle='--')
    plt.fill_between(data.index, data['UpperBand'], data['LowerBand'], alpha=0.2)
    plt.scatter(data[data['Buy_Entry']].index, data[data['Buy_Entry']]['Close'], marker='^', color='green', label='Buy Entry')
    plt.legend()
    plt.title('EMA(20) Slope, CCI(20), and Bollinger Bands(20) - Buy Entry Points')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

def main():
    ticker = 'TQQQ'
    start_date = '2018-01-01'
    end_date = '2023-08-01'
    historical_data = get_historical_data(ticker, start_date, end_date)

    # エントリーポイントを計算
    entry_points_data = calculate_entry_points(historical_data)
    # エントリーポイントをプロット
    plot_entry_points(entry_points_data)

if __name__ == "__main__":
    main()