import os
import hashlib
import time


class CacheManager:
    def __init__(self, cache_dir, cache_expiry=3600):
        self.cache_dir = cache_dir
        self.cache_expiry = cache_expiry
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate_cache_path(self, url):
        return os.path.join(self.cache_dir, hashlib.md5(url.encode()).hexdigest() + ".html")

    def is_cache_valid(self, cache_path):
        time_file_path = cache_path + ".time"
        if os.path.exists(time_file_path):
            with open(time_file_path, 'r') as f:
                timestamp = float(f.read())
            return (time.time() - timestamp) < self.cache_expiry
        return False

    def load_from_cache(self, cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()

    def update_cache(self, cache_path, content):
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(cache_path + ".time", 'w') as f:
            f.write(str(time.time()))

