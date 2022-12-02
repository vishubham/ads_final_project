import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from plotly import graph_objs as go

st.title("Stock Analysis")

stock_code = st.text_input("NYSE Stock Code:", "AMZN")
start_date = st.date_input("Start Date:", datetime.now() - timedelta(days=365))
end_date = st.date_input("End Date:", datetime.now())

# Streamlit widgets automatically run the script from top to bottom. 
# Since this button is not connected to any other logic, it just causes a plain rerun.
st.button("Analyze")

@st.cache  # Don't invoke API repeatedly with same arguments
def av_api_call(strFunc, ticker):
    url = ("https://www.alphavantage.co/query?function=" + strFunc
            + "&symbol=" + ticker
            + "&outputsize=full"  # comment this line if you only want the last 100 entries for testing purposes
            + '&apikey=C62Q8YVLLD1R9LO5'  # replace with your own free key from https://www.alphavantage.co/support/#api-key
          )
    response = requests.get(url)  # execute API call
    return response.json()  # convert json response to python dictionary

data_dict = av_api_call('TIME_SERIES_DAILY_ADJUSTED', stock_code)

# AlphaVantage changed the TIME_SERIES_DAILY API from free to chargable during the development of this project.
# Hence, we will try 2 different APIs. 
# As a last resort, we will use a historical data saved from a previous response JSON file.
if 'Information' in data_dict.keys():
    data_dict = av_api_call('TIME_SERIES_DAILY', stock_code)

# if the second API also did not work then proceed with sample data
if 'Information' in data_dict.keys():
    st.write("__API issue!__ Data for Amazon (AMZN) loaded by default.")
    data_dict = json.loads(open('./data/API Response sample AMZN.json').read())

# Convert json response into pandas dataframe
main_df = pd.DataFrame(data_dict['Time Series (Daily)'])
main_df = main_df.transpose()  # convert columns to index
main_df.columns = [s[3:] for s in main_df.columns]  # remove numbers and rename columns
main_df.index = pd.to_datetime(main_df.index)  # Correct the datatypes
main_df.index = main_df.index.date
for col in main_df.columns:
    main_df[col] = pd.to_numeric(main_df[col])

st.write("### Raw Data")
st.write(main_df.loc[end_date:start_date, :])  # Filter data for selected date range

# Plot the trend line of daily closing prices
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=main_df.loc[end_date:start_date, :].index, 
                                y=main_df.loc[end_date:start_date, 'close'], 
                                name='Daily Close Price'))
    fig.layout.update(title_text='Daily close prices for '+stock_code, 
                        xaxis_rangeslider_visible=True,
                        yaxis_title='Unit Price (USD)')
    st.plotly_chart(fig)

st.write("### Trend line")
plot_raw_data()

# Stats
st.write("### Stock Stats")

split_coeff = main_df.loc[:, 'split coefficient'].mean()
if split_coeff != 1.0:
    st.write('__Stock split alert!__  \nThe stock was split on following days:')
    st.write(main_df[main_df['split coefficient'] > 1.0])
    st.write('')

start_price = main_df.loc[:start_date, 'close'][-1]
end_price = main_df.loc[end_date:, 'close'][0]
se_diff = start_price - end_price
st.write('Price on ' + start_date.strftime("%Y-%m-%d") + ' (or next trading day): USD ' + str(start_price.round(2)))
st.write('Price on ' + end_date.strftime("%Y-%m-%d") + ' (or previous trading day): USD ' + str(end_price.round(2)))
st.write('Start-End Difference: USD ' + str(se_diff.round(2)))
st.write('')

avg_price = main_df.loc[end_date:start_date, 'close'].mean()
curr_price = main_df['close'][0]
ac_diff = avg_price - curr_price
st.write('Average price between ' + start_date.strftime("%Y-%m-%d") + ' and ' + end_date.strftime("%Y-%m-%d") + ': USD ' + str(avg_price.round(2)))
st.write('Latest price: USD ' + str(curr_price.round(2)))
st.write('Average-Current Difference: USD ' + str(ac_diff.round(2)))
