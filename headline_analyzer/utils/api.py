import pandas as pd
from newsapi import NewsApiClient
from pathlib import Path 
from dotenv import load_dotenv
import re
import os
import datetime

class ApiHandler:
    def __init__(self):
        self.newsapi = self.get_client()

    def get_client(self):
        '''Get API connection'''
        local_dir = os.path.dirname(os.path.abspath('__file__'))
        parent_dir = os.path.dirname(local_dir)
        api_env_filepath = os.path.join(parent_dir,'api.env')
        load_dotenv(Path(api_env_filepath))

        return NewsApiClient(api_key=os.getenv('NEWSAPI_API_KEY'))

    def get_headlines(self):
        '''Pull headline data'''
        top_us_headlines = self.newsapi.get_top_headlines(
            country='us',
            category='business',
            language='en',
            page_size=100
        )

        if len(top_us_headlines) == 0:
            print('Something went wrong with the api pull, no data pulled')
            return []

        top_headlines = []
        for i in top_us_headlines['articles']:
            top_headlines.append((i['title'],self.strip_date(i['publishedAt'])))

        print(f'Returning {len(top_headlines)} top us headlines')
        return top_headlines

    def strip_date(self,raw_date):
        '''Format raw date from API to y-m-d format'''
        dt = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%Y-%m-%d')

    @staticmethod
    def get_source(headline):
        '''Retrieve source of the headline'''
        if '-' in headline:
            return headline.split('-')[-1]
        return None

    @staticmethod
    def get_clean_headline(headline):
        '''Clean headline for more accurate sentiment reading'''
        # Remove source 
        if '-' in headline:
            tmp = headline.split('-')[0]
        else:
            tmp = headline

        # Remove non-alphabetic characters
        tmp = re.sub(r'[^A-Za-z0-9\s]','',tmp)
        tmp = tmp.lower()

        # Remove white space
        tmp = re.sub(r'\s+', ' ',tmp).strip()

        return tmp

    @staticmethod
    def get_keywords(headline):
        '''Pull and return list of keywords from headline'''
        pass

    @staticmethod
    def get_company(headline):
        '''Pull company mentions from headline'''
        pass