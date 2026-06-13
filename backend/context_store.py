import threading


class ContextStore:
    def __init__(self):
        self._store = {}
        self._lock = threading.Lock()

    def save(self, user_id, key, value):
        with self._lock:
            if user_id not in self._store:
                self._store[user_id] = []
            self._store[user_id].append({"key": key, "value": value})
        return True

    def list_for_user(self, user_id):
        with self._lock:
            return list(self._store.get(user_id, []))
