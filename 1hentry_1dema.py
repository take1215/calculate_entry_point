import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pytz

def get_entry_data(ticker, start_date, end_date, interval = "1h"):
    data = yf.download(ticker, start = start_date, end=end_date, interval=interval)
    return data

def calculate_ema(data, period = 20):
    ema = data['Close'].ewm(span = period, adjust = False).mean()
    return ema

def calculate_cci(data, period = 20):
    typical_price = (data["High"] + data["Low"] + data["Close"]) / 3
    cci = (typical_price - typical_price.rolling(period).mean()) / (0.015 * typical_price.rolling(period).std())
    return cci

def calculate_bollinger_bands(data, period = 20, num_std = 2):
    sma = data["Close"].rolling(period).mean()
    std = data["Close"].rolling(period).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return upper_band, lower_band

def calculate_entry_points(data):
    
    data["EMA"] = calculate_ema(data)
    data["CCI"] = calculate_cci(data)
    data["UpperBand"], data["LowerBand"] = calculate_bollinger_bands(data)
    
    # 上位足のデータを取得
    higher_timeframe_data = yf.download("SOXL", "2023-01-01", "2023-08-08", interval="1d")
    higher_timeframe_data = higher_timeframe_data.tz_localize(pytz.timezone('America/New_York')).tz_convert(pytz.UTC)
    higher_timeframe_data = higher_timeframe_data.reindex(data.index, method="ffill")
    
    higher_timeframe_ema = calculate_ema(higher_timeframe_data)
    
    # 上位足のEMAの傾きを計算
    higher_timeframe_ema_slope = higher_timeframe_ema.diff()
    print(higher_timeframe_ema_slope)
    
    for i in range(len(data)):
        if data["CCI"][i] <= -100 and data['Close'][i] <= data['LowerBand'][i] and higher_timeframe_ema_slope[i] >= -0.5:
            data.loc[data.index[i], "Buy_Entry"] = True
        else:
            data.loc[data.index[i], "Buy_Entry"] = False
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
    ticker = "SOXL"
    start_date = "2023-01-01"
    end_date = "2023-08-08"
    historical_data = get_entry_data(ticker, start_date, end_date)
    
    entry_points_data = calculate_entry_points(historical_data)
    
    plot_entry_points(entry_points_data)

if __name__ == "__main__":
    main()







    
#1h足 ：：米国の場合一日6時間半取引可 一日7本 730/7 = 104.xxxx 104日まで