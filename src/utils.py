import logging
from cachetools import cached, LRUCache

# Configure logging format (global)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

@cached(cache=LRUCache(maxsize=64))
def cached_read(file_path: str) -> str:
    """Reads a file and caches the content."""
    with open(file_path, 'r') as f:
        return f.read()
