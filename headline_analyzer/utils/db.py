from dataclasses import dataclass
from google.cloud import storage
import os
import sqlite3
import json

@dataclass
class DataBaseModelConfig:
    bucket_name: str
    model_name: str

@dataclass
class DataBaseSQLConfig:
    bucket_name: str
    db_file: str
    table_name: str
    local_db_path: str

class DataBaseModelHandler:
    def __init__(self,config):
        self.config = config
        self.init_google_conn()

    def init_google_conn(self):
        client = storage.Client()
        bucket = client.get_bucket(self.config.bucket_name)
        self.blob = bucket.blob(self.config.model_name)

    def download_blob(self) -> bool:
        if self.blob.exists():
            self.blob.download_to_filename(self.config.model_name)
            return True
        else:
            return False

    def remove_local_blob(self) -> bool:
        try:
            for filename in os.listdir(self.config.model_name):
                file_path = os.path.join(self.config.model_name,filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'[DB] {filename} removed from dir')
            return True
        except:
            print(f'[DB] {self.config.model_name} not found')
            return False

class DataBaseSQLHandler:
    def __init__(self,config):
        self.config = config
        self.download_db()

    def download_db(self) -> bool:
        """Inits connection to google cloud and downloads db file"""
        client = storage.Client()
        bucket = client.get_bucket(self.config.bucket_name)
        self.blob = bucket.blob(self.config.db_file)

        if self.blob.exists():
            self.blob.download_to_filename(self.config.local_db_path)
            print(f'[DB] Downloaded {self.config.db_file} from bucket {self.config.bucket_name} to {self.config.local_db_path}')
            return True
        
        print(f'[DB] No database file found in bucket {self.config.bucket_name}')
        return False

    def push_db(self):
        """Uploads db file back to google cloud"""
        self.blob.upload_from_filename(self.config.local_db_path)
        print(f'[DB] Uploaded {self.config.db_file} to {self.config.bucket_name}')
    
    def create_or_update_db(self, data=None):
        """Creates a new databse or updates the existing one"""
        conn = sqlite3.connect(self.config.local_db_path)
        cursor = conn.cursor()

        # Create a table if it doesn't exist
        cursor.execute(f'''
           CREATE TABLE IF NOT EXISTS '{self.config.table_name}' (
            Key NVARCHAR(64) PRIMARY KEY,
            Headline TEXT NOT NULL,
            Sentiment INTEGER NOT NULL,
            Company TEXT,
            Keywords TEXT NOT NULL,
            Source TEXT,
            Date DATE
           )
        ''')

        print(f'[DB] Adding unique data to {self.config.table_name}')
        for _,rows in data.iterrows():
            row_data = (rows['key'],rows['headline'],rows['sentiment'],rows['company'],json.dumps(rows['keywords']),rows['source'],rows['date'])

            # Check if headline already exists based on Key
            cursor.execute(f'''
                SELECT COUNT(*) FROM {self.config.table_name} WHERE Key = ?
            ''',(rows['key'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute(f'''
                    INSERT INTO '{self.config.table_name}' (Key,Headline,Sentiment,Company,Keywords,Source,Date) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',row_data)
            else:
                dup_headline = rows['headline']
                print(f'Headline already exists: {dup_headline}')

        conn.commit()
        cursor.close()
        conn.close()