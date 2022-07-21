from typing import Optional
from google.cloud import storage
from threading import Lock

from config import Config
from storage.storage import Storage


class GoogleCloudStorage(Storage):
    file_lock = Lock()  # This helps prevent concurrency issues from this crude approach
    bucket = Config.get_bucket()

    def __init__(self, bucket: Optional[str] = None):
        self.bucket = bucket or Config.get_bucket()
        self.client = storage.Client()

    def read_file(self, filename: str) -> str:
        with self.file_lock:
            return (
                self.client.bucket(self.bucket)
                .blob(filename)
                .download_as_bytes()
                .decode("UTF-8")
            )

    def write_file(self, filename: str, content: str):
        with self.file_lock:
            self.client.bucket(self.bucket).blob(filename).upload_from_string(content)

    def delete_file(self, filename: str):
        with self.file_lock:
            self.client.bucket(self.bucket).blob(filename).delete()

    def exists(self, filename: str) -> bool:
        with self.file_lock:
            return self.client.bucket(self.bucket).get_blob(filename) is not None
