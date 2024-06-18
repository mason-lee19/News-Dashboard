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