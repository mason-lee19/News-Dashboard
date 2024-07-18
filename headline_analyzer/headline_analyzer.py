'''
This folder will serve as the code to collect headline data, analyze the sentiment, extract keywords and companies from headlines, and then upload to database file in the google cloud model.

All code will be within this folder to differentiate for cron job upload.
'''
import os
import requests

from newsapi import NewsApiClient
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import numpy as np

from utils.api import ApiHandler
from utils.db import DataBaseModelConfig, DataBaseSQLConfig, DataBaseModelHandler, DataBaseSQLHandler
from utils.model import SentimentModel


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "news-dashboard-428816-944234361d91.json"

def main():
    # Check and setup Model
    print('[MAIN] Setting up Sentiment model')
    model = SentimentModel('sentiment_model')
    id2label = model.model.config.id2label

    # Pull new headline data
    print('[MAIN] Pulling headline data')
    news_api = ApiHandler()
    headlines,dates = news_api.get_headlines()
    top_headlines = pd.concat([headlines,dates],axis=1)
    print(f'[MAIN] Pulled {len(top_headlines)} headlines')

    # Key | Headline | Sentiment | Company | Keywords | Source | Date

    # Create index keys based on serialized raw headlines
    print('[MAIN] Serializing headlines')
    top_headlines['key'] = top_headlines['headline'].apply(news_api.serialize_headline)
    # Clean headlines
    print('[MAIN] Cleaning headlines for sentiment model')
    top_headlines['clean_headlines'] = top_headlines['headline'].apply(news_api.get_clean_headline)
    # Clean date
    print('[MAIN] Cleaning date')
    top_headlines['date'] = top_headlines['date'].apply(news_api.strip_date)
    # Pull source
    print('[MAIN] Pulling source from raw headline')
    top_headlines['source'] = top_headlines['headline'].apply(news_api.get_source)

    # Pass headline data through Model to get sentiment
    print('[MAIN] Analyzing sentiment of cleaned headlines')
    batch_sentences = top_headlines.sample(n=len(top_headlines),random_state=1)['clean_headlines'].to_list()
    batch_sentence_probas = model.batch_predict_proba(batch_sentences)
    top_headlines['sentiment'] = [id2label[i] for i in np.argmax(batch_sentence_probas,axis=1)]

    # Collect key words
    print('[MAIN] Collecting keywords from cleaned headlines')
    top_headlines['keywords'] = top_headlines['clean_headlines'].apply(news_api.get_keywords)

    # Parse keywords for companies
    print('[MAIN] Finding correlated companies')
    top_headlines['company'] = top_headlines['keywords'].apply(news_api.get_company)

    top_headlines.to_csv('data.csv')

    # Pull cloud db file, update with new data, push new db file to cloud
    dbConfig = DataBaseSQLConfig(
        bucket_name='news-headline-data',
        db_file='data.db',
        table_name='headline_data',
        local_db_path='tmp/data.db'
        )
    
    dbHandler = DataBaseSQLHandler(dbConfig)
    print(f'[MAIN] Pushing {dbConfig.db_file} to {dbConfig.bucket_name}')
    dbHandler.download_db()
    dbHandler.create_or_update_db(top_headlines[[
        'key',
        'headline',
        'sentiment',
        'company',
        'keywords',
        'source',
        'date'
        ]])
    dbHandler.push_db()


if __name__ == "__main__":
    main()