from dataclasses import dataclass

import os
from pathlib import Path
from dotenv import load_dotenv

import alpaca_trade_api as tradeapi
import pandas as pd

@dataclass
class ApiConfig:
    api_key: str
    api_secret: str
    base_url: str

class GetStockData:
    def __init__(self):
        self.apiConfig = self.configure_api()

    def configure_api(self) -> ApiConfig:
        local_dir = os.path.dirname(os.path.abspath('__file__'))
        config_file_path = os.path.join(local_dir,'api.env')
        load_dotenv(Path(config_file_path))

        apiConfig = ApiConfig(api_key=os.getenv("API_KEY"),
                              api_secret=os.getenv("API_SECRET"),
                              base_url=os.getenv("BASE_URL"))

        return apiConfig

    def init_api(self):
        self.api = tradeapi.REST(self.apiConfig.api_key, self.apiConfig.api_secret, self.apiConfig.base_url, api_version='v2')

    def get_data(self,ticker:str,timeframe:str,startdate:str=None,enddate:str=None):
        bars = self.api.get_barset(ticker,timeframe,start=startdate,end=enddate)
        bars_df = bars.df

        return bars_df

    def calc_returns(self,data,timeframe:int=1):
        pass

    