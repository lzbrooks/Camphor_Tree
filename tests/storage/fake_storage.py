from threading import Lock
from storage.storage import Storage


class FakeStorage(Storage):

    file_lock = Lock()
    temp_file_system = {}

    def read_file(self, filename: str) -> str:
        with self.file_lock:
            return self.temp_file_system.get(filename)

    def write_file(self, filename: str, content: str):
        with self.file_lock:
            self.temp_file_system[filename] = content

    def delete_file(self, filename: str):
        with self.file_lock:
            del self.temp_file_system[filename]

    def exists(self, filename: str) -> bool:
        with self.file_lock:
            return filename in self.temp_file_system
