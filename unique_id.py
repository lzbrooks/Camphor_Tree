from threading import Lock
from storage.google_storage import GoogleCloudStorage

UNIQUE_ID_FILENAME = "unique_id.txt"
unique_id_lock = Lock()

storage = GoogleCloudStorage()
def get_next_unique_id():
    with  unique_id_lock:
        unique_id = storage.read_file(UNIQUE_ID_FILENAME)
        if unique_id is None:
            unique_id = 0
        else:
            unique_id = (unique_id + 1) % 0b1111111
        storage.write_file(UNIQUE_ID_FILENAME, unique_id)
        return unique_id