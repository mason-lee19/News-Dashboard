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


def main():
    print('Started Main')

    # Check and setup Model

    # Pull new headline data

    # Pass headline data through Model to get sentiment

    # Collect key words

    # Parse keywords for companies

    # Serialize headline through hashlib.sha256(headline.encode('utf-8')).hexdigest()
    # will create unique identifier based on headline so we can avoid adding duplicates

    # Key | Headline | Sentiment | Company | Keywords | Source | Date

    # Push new data to db file and upload

if __name__ == "__main__":
    main()