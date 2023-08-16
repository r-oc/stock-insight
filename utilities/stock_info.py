from datetime import date
import yfinance as yf
import pandas as pd


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 30)

    print("welcome.")

    # THESE WILL BE INPUTS
    ticker = "JNJ"
    start_date = "1962-02-13"
    end_date = "2023-02-18"
    reinvest = True
    shares = 1000

    data = yf.Ticker(ticker).history(start=date(1962, 2, 13))
    df = pd.DataFrame(columns=['Date', 'Shares', 'Total Value'])

    print(yf.download(ticker, date(1962, 2, 13)))
    print("\n\nNEXT!\n\n")
    print(data)

    # print(type(data))
    # print(data['Close'])
    # print("\n------------------------------------\n")
    # print(data['Dividends'])

    balance = 0
    dividend_sum = 0
    for date, row in data.iterrows():
        stock_price = row['Close']
        total_value = stock_price * shares

        dividend_paid = row['Dividends']
        if dividend_paid > 0:
            # print(date, stock_price, dividend_paid, balance, shares)
            total_dividend = dividend_paid * shares
            drip = (total_dividend + balance) // stock_price

            balance += total_dividend - (drip * stock_price)
            shares += int(drip)

            while balance >= stock_price:
                balance -= stock_price
                shares += 1

        # ADD ROW


