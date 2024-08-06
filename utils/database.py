from dataclasses import dataclass
from google.cloud import storage
import sqlite3
import pandas as pd

@dataclass
class DataBaseSQLConfig:
    bucket_name: str
    db_file: str
    table_name: str
    local_db_path: str

class DataBaseSQLHandler:
    def __init__(self,config):
        self.config = config

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
    
    def pull_data(self) -> pd.DataFrame():
        conn = sqlite3.connect(self.config.local_db_path)

        df = pd.read_sql_query(
            '''SELECT * 
            FROM headline_data 
            ORDER BY Date DESC
            LIMIT 50'''
            ,conn)

        if len(df) == 0:
            print(f'[DB] Length of data from {self.config.local_db_path} is equal to 0')
        else:
            print(f'[DB] Pull from {self.config.local_db_path} successful')
            print(f'[DB] Length of Data: {len(df)} rows')

        conn.close()

        return df
