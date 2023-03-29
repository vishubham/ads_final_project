# ads_final_project
Stock Investment Analysis Tool

Shubham Saurabh
Luddy School of Informatics, Computing, and Engineering, Indiana University, Bloomington
DSCI D590 Applied Data Science
Dr. Olga Scrivner
October 1, 2022

Updated on Mar-29-2023

# Description
The average retail stock trader or investor has little knowledge about investing and virtually no access to advanced stock data analysis tools. This project aims to provide a useful tool that can be used by retail investors to analyze stock market data and make informed investment decisions.

# Objective
Now a days several apps (e.g., Robinhood, Webull, etc.) have emerged that enable regular folks, i.e., retail investors with small amounts of money, to easily invest in publicly traded stocks. While the trading part has been made easy by these tools, little has been done to educate these small investors and help them in deciding which stocks to buy or sell and when.
The main objective of this project is to develop a stock market data analysis tool that can be used by retail investors to identify long term investment opportunities in stocks traded on the New York Stock Exchange (NYSE). Once we establish a working model that works for long term investors, the tool can be further developed to add enhanced capabilities to handle instantaneous data analysis for use in day trades. 

# Dataset
The primary objective is to make the tool work on real data fetched by using free APIs provided by companies like:
•	Google Finance: https://support.google.com/docs/answer/3093281?hl=en 
•	Alpha Vantage: https://www.alphavantage.co/documentation/
These APIs provide data in JSON format which is easily readable for both humans and machine. The data will not need any cleanup activities as the service providers take care of missing data.

However, in case we are unable to setup real-time data fetching due to technical challenges, the backup plan is to utilize the Kaggle dataset of New York Stock Exchange (Gawlik, 2017) to perform the same operations with a static dataset. In this approach the source files can be updated with latest data on a regular basis to provide updated results. Details about NYSE Kaggle dataset:
•	Publisher: Dominik Gawlik
•	Published date: 2017, February 22
•	Data Source: Prices were fetched from Yahoo Finance, Fundamentals are from Nasdaq Financials, extended by some fields from EDGAR SEC databases.
We will utilize only one of the four files in the dataset i.e., prices.csv. The data has been preprocessed before publishing; hence there is no missing data, and no data cleanup will be required. Overall, the file has 851264 records – one for each day of trading from 2010 to 2016 for 501 stock codes. Only the following columns will be utilized in the project:
•	date: Date of stock price details. All trading dates when the NYSE was open from 2010 to 2016 are present.
•	symbol: NYSE code of the stock we want to analyze
•	close: The closing price of the stock at end of business day
•	volume: Count of shares of the stock traded on the given business day

# Functionalities
The following core functionalities will be offered by the web app:
Data Science Function
1.	Visualization: The users would be able to fetch and visualize the historical trend line for any specified stock listed on the NYSE within a specified date range.
2.	Stock Analysis: The user would be able to fetch and view the average price of a specified stock within a specified date range and compare it to the current market price of the stock.
User Interaction
1.	The web app will allow the users to specify the inputs like: 
a.	Stock code
b.	Starting Date
c.	Ending Date
2.	The web app will display the outputs including graphs and text in a colorblind friendly view.

# References
Gawlik, D. (2017, February 22). Kaggle dataset - New York Stock Exchange. Kaggle. Retrieved October 11, 2022, from https://www.kaggle.com/datasets/dgawlik/nyse 
Horvath, S. (2022, August 29). 9 Best stock research tools. Retrieved October 11, 2022, from https://www.benzinga.com/money/stock-research-tools 
