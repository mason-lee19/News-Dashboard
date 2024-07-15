# News-Dashboard

This project is to setup the scripts necessary to extract, transform, and load financial news data and create an analytical dashboard.

# Capabilities

- Extract transform and upload digested financial news data
  - Pull headline data from NewsAPI
  - Digest and upload to SQL db in Google Cloud
  - Key | Headline | Sentiment | Company | Keywords | Source | Date
 
- Train and implement a sentiment model to analyze sentiment of headlines * Done

- headline_analyzer folder will contain all the necessary code to package and implement to a cron job in google cloud

- Once data is uploaded, dashboard just needs to pull and process the data in order to summarize

- Stock data will be pulled from yfinance and alpaca api to update tracked stocks on the dashboard * Done
  - YF is used for daily data while alpaca is better for 2D - 5Yr, without a subscription we can't pull current day data from alpaca

# Dashboard gui design

![Dashboard gui](attachments/News-Dash-GUI.png)
