from typing import Any


class ChainingHashTable:
    """
    A simple hash table implementation using separate chaining.

    Separate chaining stores multiple key-value pairs in each bucket as a Python list to handle hash
    collisions. If two keys hash to the same bucket index, they coexist in the same bucket list.
    """

    def __init__(self, initial_capacity: int = 20) -> None:
        """
        Initializes the hash table with a fixed number of buckets.
        """
        # Each bucket is itself a list that stores key-value pairs.
        self.list: list[list[list[Any]]] = [[] for _ in range(initial_capacity)]

    def _find_pair(self, key: Any) -> tuple[list[Any] | None, list[list[Any]]]:
        """
        Internal helper: locate the key's [key, value] pair, and its bucket.
        """
        bucket_index = hash(key) % len(self.list)
        bucket = self.list[bucket_index]

        for pair in bucket:
            if pair[0] == key:
                return pair, bucket
        return None, bucket

    def insert(self, key: Any, item: Any) -> bool:
        """
        Insert or update a key-value pair.
        """
        pair, bucket = self._find_pair(key)
        if pair:
            pair[1] = item  # update existing
        else:
            bucket.append([key, item])  # insert new
        return True

    def lookup(self, key: Any) -> Any | None:
        """
        Retrieves a value by key.
        """
        pair, _ = self._find_pair(key)
        return pair[1] if pair else None

    def hash_remove(self, key: Any) -> bool:
        """
        Remove a key-value pair by key.
        """
        pair, bucket = self._find_pair(key)
        if pair:
            bucket.remove(pair)
            return True
        return False