import pandas as pd
from newsapi import NewsApiClient
from pathlib import Path 
from dotenv import load_dotenv
import re
import os
from datetime import datetime
import hashlib

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

HEADLINES_PER_PULL = 100


class ApiHandler:
    def __init__(self):
        self.newsapi = self.get_client()
        sp_data_df = pd.read_csv('sp500.csv')[['Name','Symbol']]
        self.sp_dict = {row['Name'].lower().replace(' ',''):row['Symbol'] for _,row in sp_data_df.iterrows()}


    def get_client(self):
        '''Get API connection'''
        local_dir = os.path.dirname(os.path.abspath('__file__'))
        api_env_filepath = os.path.join(local_dir,'news_api.env')
        load_dotenv(Path(api_env_filepath))

        return NewsApiClient(api_key=os.getenv('NEWSAPI_API_KEY'))

    def get_headlines(self):
        '''Pull headline data'''
        top_us_headlines = self.newsapi.get_top_headlines(
            country='us',
            category='business',
            language='en',
            page_size=HEADLINES_PER_PULL
        )

        if len(top_us_headlines) == 0:
            print('[API] Something went wrong with the api pull, no data pulled')
            return []

        top_headlines = []
        headline_dates = []
        for i in top_us_headlines['articles']:
            top_headlines.append(i['title'])
            headline_dates.append(i['publishedAt'])

        print(f'[API] Returning {len(top_headlines)} top us headlines')
        return pd.DataFrame(top_headlines,columns=['headline']), pd.DataFrame(headline_dates,columns=['date'])

    @staticmethod
    def strip_date(raw_date):
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
    def serialize_headline(headline):
        '''Serialize headline to be used as key'''
        headline_bytes = headline.encode('utf-8')

        sha256_hash = hashlib.sha256()
        sha256_hash.update(headline_bytes)

        unique_key = sha256_hash.hexdigest()

        return unique_key

    @staticmethod
    def get_keywords(headline):
        '''Pull and return list of keywords from headline'''
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(headline)
        keywords = [word for word in word_tokens if word.isalpha() and word.lower not in stop_words]

        return keywords

    def get_company(self,keywords):
        '''Pull company mentions from headline'''
        for word in keywords:
            if word in self.sp_dict:
                return self.sp_dict[word]
            elif word[:-1] in self.sp_dict:
                return self.sp_dict[word[:-1]]
        return 'general'