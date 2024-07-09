from dataclasses import dataclass
from google.cloud import storage

@dataclass
class DataBaseModelConfig:
    bucket_name: str
    model_name: str

@dataclass
class DataBaseFileConfig:
    bucket_name: str
    db_file: str
    url: str
    table_name: str

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
            os.remove(self.config.blob_name)
            print(f'{self.config.blob_name} removed from dir')
            return True
        except:
            print(f'{self.config.blob_name} not found')
            return False