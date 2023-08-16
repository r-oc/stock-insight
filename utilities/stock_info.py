from datetime import date
import yfinance as yf
import pandas as pd


def get_stock_frame(ticker, start_date, end_date, reinvest, shares):
    print('hi')
    df = pd.DataFrame(columns=['Date', 'Shares', 'Total Value', 'Dividend Yield'])

    # Unfortunately yfinance doesn't allow you to get Close price in their Ticker.history() method and yf.download()
    # doesn't give you dividend data =(
    dividend_data = yf.Ticker(ticker).history(start=start_date, end=end_date)['Dividends']
    price_data = yf.download(tickers=ticker, start=start_date, end=end_date)

    balance = 0
    dividend_sum = 0
    for i, row in enumerate(price_data.iterrows()):
        date = str(row[0])[:10]
        stock_price = row[1]['Close']
        total_value = stock_price * shares

        new_row = {'Date': date, 'Shares': shares, 'Total Value': total_value, 'Dividend Yield': dividend_sum}
        df.loc[len(df)] = new_row

        dividend_paid = dividend_data[i]
        dividend_sum += dividend_paid * shares
        if reinvest and dividend_paid > 0:
            total_dividend = dividend_paid * shares
            drip = (total_dividend + balance) // stock_price

            balance += total_dividend - drip * stock_price

            shares += int(drip)
            while balance >= stock_price:
                balance -= stock_price
                shares += 1

    return df


# if __name__ == '__main__':
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_rows', 30)
#
#     print("welcome.")
#
#     # THESE WILL BE INPUTS
#     ticker2 = "JNJ"
#     start_date2 = date(1962, 2, 13)
#     end_date2 = date.today()
#     reinvest2 = True
#     shares2 = 1000
#
#     df2 = get_stock_frame(ticker2, start_date2, end_date2, reinvest2, shares2)
#
