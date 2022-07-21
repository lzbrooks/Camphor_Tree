import os
import pathlib
from threading import Lock

from storage.storage import Storage


class LocalStorage(Storage):
    file_lock = Lock()  # This helps prevent concurrency issues from this crude approach

    def __init__(self, directory: str):
        if os.path.isfile(directory):
            raise ValueError(directory, "is a file, not a directory")
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.directory = pathlib.Path(directory)

    def read_file(self, filename: str) -> str:
        with self.file_lock:
            with open(self.directory / filename, "r") as f:
                return f.read()

    def write_file(self, filename: str, content: str):
        with self.file_lock:
            with open(self.directory / filename, "w") as f:
                f.write(content)

    def delete_file(self, filename: str):
        with self.file_lock:
            os.remove(self.directory / filename)

    def exists(self, filename: str) -> bool:
        with self.file_lock:
            return os.path.isfile(self.directory / filename)
