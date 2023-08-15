import yfinance as yf
import pandas as pd
import streamlit as st

if __name__ == '__main__':
    st.set_page_config(page_title="Stock Insight", page_icon="images/tab_logo.jpg")

    st.title('Hello World!\n')
    st.write('Hello, this is a message.')

    st.sidebar.header('This is a sidebar.')
    st.sidebar.text_input("Input 1", "Hi")
    st.sidebar.text_input("Input 2", "Bye")