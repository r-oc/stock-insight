from datetime import date

import requests
import streamlit as st
import yfinance as yf
import pandas as pd

if __name__ == '__main__':
    st.set_page_config(page_title='Stock Insight', page_icon='images/tab_logo.jpg')

    st.title('Stock Insight')
    st.write('Track historical stock information and calculate holding positions including dividend reinvestment.')

    # Build Sidebar
    st.sidebar.header('Enter stock information...')

    ticker = st.sidebar.text_input(
        label='Stock Symbol',
        value='AAPL'
    )

    try:
        info = yf.Ticker(ticker).info
    except requests.exceptions.HTTPError:
        st.sidebar.write('* Invalid stock symbol, defaulting to AAPL.')
        ticker = 'AAPL'

    start_date = st.sidebar.date_input(
        label='Start Date',
        format='YYYY-MM-DD',
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        value=date(2022, 1, 1)
    )

    end_date = st.sidebar.date_input(
        label='End Date',
        format='YYYY-MM-DD',
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        value=date.today()
    )

    reinvest = st.sidebar.radio(
        label='Handle Dividends',
        options=['Reinvest', 'Save as cash']
    )
    reinvest = True if reinvest == "Reinvest" else False

    investment_type = st.sidebar.radio(
        label='Type of investment',
        options=['Shares', 'Cash']
    )

    # Avoid any undefined errors, even though shares would always be calculated.
    shares = 1000
    cash_invested = 1000

    if investment_type == 'Shares':
        shares = int(st.sidebar.text_input(
            label='Shares Invested',
            value=1000
        ))
    else:
        cash_invested = int(st.sidebar.text_input(
            label=f'Cash invested on {start_date}',
            value=1000
        ))

    # Frame that will store data for tables.
    df = pd.DataFrame(columns=['Date', 'Shares', 'Total Value', 'Dividend Yield', 'Stock Value'])

    with st.spinner('Downloading stock data...'):
        dividend_data = yf.Ticker(ticker).history(start=start_date, end=end_date)['Dividends']
        price_data = yf.download(tickers=ticker, start=start_date, end=end_date)

    # if investment_type is cash, calculate shares.
    if investment_type == 'Cash':
        stock_price_day_one = price_data['Close'][0]
        shares = int(cash_invested / stock_price_day_one)

    if shares < 0:
        shares = 1000

    with st.spinner('Calculating returns...'):

        start_value = price_data['Close'][0] * shares

        balance = 0
        dividend_sum = 0
        total_value = 0
        for i, row in enumerate(price_data.iterrows()):
            date = str(row[0])[:10]
            stock_price = row[1]['Close']
            total_value = stock_price * shares

            new_row = {'Date': date, 'Shares': shares, 'Total Value': total_value, 'Dividend Yield': dividend_sum, 'Stock Value': stock_price}
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

        df.set_index('Date', inplace=True)

        st.subheader('Total Portfolio Value')
        st.line_chart(df['Total Value'])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Stock Price')
            st.line_chart(df['Stock Value'])

        with col2:
            st.subheader('Total Shares')
            st.line_chart(df['Shares'])

        start_value = round(start_value, 2)
        total_value = round(total_value, 2)
        dividend_sum = round(dividend_sum, 2)

        st.sidebar.write('Starting Value: $', start_value)
        st.sidebar.write('Current Value: $', total_value)
        st.sidebar.write('Dividend Yield $', dividend_sum)
        st.sidebar.write('Current Shares: ', shares)

        st.toast('Stock information loaded!')
