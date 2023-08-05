import yfinance as yf
import matplotlib.pyplot as plt

def plot_stock_data(stock_symbol, interval, subplot_position):
    # Yahoo Financeからデータを取得
    stock_data = yf.download(stock_symbol, period='1mo', interval=interval)

    # サブプロットの設定
    plt.subplot(3, 1, subplot_position)
    plt.plot(stock_data['Close'], label='Close', linewidth=2)
    plt.title(f'{stock_symbol}: {interval}', fontsize=12)
    plt.xlabel('date', fontsize=10)
    plt.ylabel('price', fontsize=10)
    plt.legend(loc='best')
    plt.grid(True)

if __name__ == "__main__":
    # 株価情報をプロットする対象の銘柄（SOXL）
    stock_symbol = 'SOXL'

    # サブプロットで上、中央、下に日足、一時間足、90分足をプロット
    plt.figure(figsize=(12, 18))
    plt.subplots_adjust(hspace=0.5)

    intervals = ['1d', '1h', '15m']
    for i, interval in enumerate(intervals, start=1):
        plot_stock_data(stock_symbol, interval, i)

    plt.show()