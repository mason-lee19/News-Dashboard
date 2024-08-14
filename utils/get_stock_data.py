from dataclasses import dataclass

from .tools import Utils

import os
from pathlib import Path
from dotenv import load_dotenv

import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd

@dataclass
class ApiConfig:
    api_key: str
    api_secret: str
    base_url: str

class GetStockData:
    def __init__(self,initAlpaca):
        if initAlpaca:
            self.apiConfig = self.configure_alpaca_api()

            self.init_alpaca_api()
        

    def configure_alpaca_api(self) -> ApiConfig:
        print('[SD] Getting API info from api.env file')
        local_dir = os.path.dirname(os.path.abspath('__file__'))
        config_file_path = os.path.join(local_dir,'api.env')
        load_dotenv(Path(config_file_path))

        apiConfig = ApiConfig(api_key=os.getenv("API_KEY"),
                              api_secret=os.getenv("API_SECRET"),
                              base_url=os.getenv("BASE_URL"))

        return apiConfig

    def init_alpaca_api(self):
        print('[SD] Initializing trade api')
        self.api = tradeapi.REST(self.apiConfig.api_key, self.apiConfig.api_secret, self.apiConfig.base_url, api_version='v2')

    def get_data(self,ticker:str,period:str):
        cur_date = Utils.get_cur_date()
        
        if period == '1D':
            bars_df = yf.download(ticker,start=cur_date,interval='1m')
        else:
            startdate = Utils.calc_datetime(period)
            bars_df = self.api.get_bars(ticker,timeframe='1D',start=startdate).df
        
        return bars_df

    def get_yf_close(self,df):
        return df['Close']

    def get_alpaca_close(self,df):
        return df['close']

    def calc_returns(self,data):
        # When pulling from DB need to remember to do the same datetime calc
        return ((data.iloc[-1] - data.iloc[0])/data.iloc[0])*100

    @staticmethod
    def get_put_call_ratio(ticker):
        options_data = yf.Ticker(ticker).option_chain()
        calls = options_data.calls
        puts = options_data.puts

        return puts['volume'].sum() / calls['volume'].sum()


    