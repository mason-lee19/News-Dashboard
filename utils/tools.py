
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Utils():

    @staticmethod
    def convert_time_frame(timeframe:str='1D') -> int:
        '''
        Returns int value when inputting chosen time frame
        '''
        match timeframe:
            case '1D':
                return 1
            case '1W':
                return 5
            case '1M':
                return 21
            case '3M':
                return 63
            case '6M':
                return 126
            case '1Y':
                return 252
            case '5Y':
                return 1260

    @staticmethod
    def get_color(percentage) -> str:
        if percentage >= 0:
            return 'green'
        return 'red'

    @staticmethod
    def get_cur_date() -> str:
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def calc_datetime(period:str) -> str:
        cur_date = datetime.today()

        match period:
            case '5Y':
                return (cur_date - relativedelta(years=5)).strftime('%Y-%m-%d')
            case '1Y':
                return (cur_date - relativedelta(years=1)).strftime('%Y-%m-%d')
            case '6M':
                return (cur_date - relativedelta(months=6)).strftime('%Y-%m-%d')
            case '3M':
                return (cur_date - relativedelta(months=3)).strftime('%Y-%m-%d')
            case '1M':
                return (cur_date - relativedelta(months=1)).strftime('%Y-%m-%d')
            case '1W':
                return (cur_date - relativedelta(weeks=1)).strftime('%Y-%m-%d')
        
        print(f'Error for time: {period}')
        print('Unrecognized time detected in get_stock_data.py calc_datetime() function')

        return None