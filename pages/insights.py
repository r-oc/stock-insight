from datetime import date
import streamlit as st

if __name__ == '__main__':
    st.set_page_config(page_title="Stock Insight", page_icon="images/tab_logo.jpg")

    st.title('Stock Insight')
    st.write('Track historical stock information and calculate holding positions including dividend reinvestment.')

    # Build Sidebar
    st.sidebar.header('Enter stock information...')

    stock_symbol = st.sidebar.text_input(
        label="Stock Symbol",
        value="AAPL"
    )

    start_date = st.sidebar.date_input(
        label="Start Date",
        format="YYYY-MM-DD",
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        value=date(1900, 1, 1)
    )

    end_date = st.sidebar.date_input(
        label="End Date",
        format="YYYY-MM-DD",
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        value=date.today()
    )

    handle_dividends = st.sidebar.radio(
        label="Handle Dividends",
        options=["Reinvest", "Save as cash"]
    )

    shares_invested = st.sidebar.text_input(
        label="Shares Invested",
        value=1000
    )

    # st.write(stock_symbol, start_date, end_date, handle_dividends, shares_invested)
