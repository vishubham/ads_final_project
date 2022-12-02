# Code adapted from https://www.youtube.com/watch?v=0E_31WqVzCY

import streamlit as st
from datetime import date, timedelta
import yfinance as yf
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly

st.title("Stock Price Prediction")

stock_code = st.text_input("NYSE Stock Code:", "AMZN")
start_date = st.date_input("Start Date:", date.today() - timedelta(days=3650))
start_date = start_date.strftime("%Y-%m-%d")
today_date = date.today().strftime("%Y-%m-%d")

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Streamlit widgets automatically run the script from top to bottom. 
# Since this button is not connected to any other logic, it just causes a plain rerun.
st.button("Predict")

@st.cache
def load_data(ticker, start_date, today_date):
    data = yf.download(ticker, start_date, today_date)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Loading data.....')
data = load_data(stock_code, start_date, today_date)
data_load_state.text('Data load complete.')

st.subheader('Raw Data')
st.write(data)

# Plot the trend line of daily closing prices
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], 
                                y=data['Close'], 
                                name='Daily Close Price'))
    fig.layout.update(title_text='Daily close prices for '+stock_code, 
                        xaxis_rangeslider_visible=True,
                        yaxis_title='Unit Price (USD)')
    st.plotly_chart(fig)

st.subheader('Trend line')
plot_raw_data()

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})

model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)

st.subheader('Forecasted Data')
st.write(forecast)

st.subheader('Forecasted Trend line')
fig_forecast = plot_plotly(model, forecast)
fig_forecast.layout.update(title_text='Daily close price predictions for '+stock_code, 
                            xaxis_rangeslider_visible=True,
                            xaxis_title='ds = Timeline',
                            yaxis_title='y = Unit Price (USD)')
st.plotly_chart(fig_forecast)

st.write('Forecast Components')
fig2 = model.plot_components(forecast)
st.write(fig2)
