from typing import Any

class ChainingHashTable:
    """
    A simple hash table implementation using separate chaining.

    Separate chaining stores multiple key-value pairs in each bucket as a Python list to handle hash
    collisions. If two keys hash to the same bucket index, they coexist in the same bucket list.

    Hash tables provide approximately O(1) average time complexity for insert, lookup, and remove operations
    under uniform hashing. In the worst case (all keys collide into the same bucket), these operations
    degrade to O(N), where N is the number of keys in that bucket.
    """

    def __init__(self, initial_capacity: int = 20) -> None:
        """
        Initializes the hash table with a fixed number of buckets.

        Each bucket is implemented as a list of key-value pairs. The hash function maps keys to bucket indices.

        Time Complexity: O(initial_capacity) for initializing the bucket lists.
        """
        self.list: list[list[list[Any]]] = [[] for _ in range(initial_capacity)]

    def _find_pair(self, key: Any) -> tuple[list[Any] | None, list[list[Any]]]:
        """
        Internal helper: locate the key's [key, value] pair and its bucket.

        Algorithm:
        1. Compute the bucket index as hash(key) % number_of_buckets.
        2. Iterate through the bucket's list of [key, value] pairs.
        3. If a pair with the matching key is found, return it with the bucket.
        4. If not found, return None with the bucket for potential insertion.

        Time Complexity: O(M) where M is the number of items in the bucket.
        Best Case: O(1) if the key is first or bucket is empty.
        Worst Case: O(N) if all N items are in the same bucket.
        """
        bucket_index = hash(key) % len(self.list)
        bucket = self.list[bucket_index]

        for pair in bucket:
            if pair[0] == key:
                return pair, bucket
        return None, bucket

    def insert(self, key: Any, item: Any) -> bool:
        """
        Insert a new key-value pair or update an existing key's value.

        Algorithm:
        1. Use _find_pair to locate if the key exists in its bucket.
        2. If the key exists, update its value.
        3. If not, append a new [key, value] pair to the bucket list.

        Time Complexity: O(M) for _find_pair, where M is the bucket size.
        Average Case: O(1) assuming uniform hashing and low load factor.
        Worst Case: O(N) if all keys collide in the same bucket.
        """
        pair, bucket = self._find_pair(key)
        if pair:
            pair[1] = item  # update existing
        else:
            bucket.append([key, item])  # insert new
        return True

    def lookup(self, key: Any) -> Any | None:
        """
        Retrieve the value associated with a key.

        Algorithm:
        1. Use _find_pair to locate the key in its bucket.
        2. Return the value if found, otherwise return None.

        Time Complexity: O(M) where M is the bucket size.
        Average Case: O(1)
        Worst Case: O(N) if all keys collide in the same bucket.
        """
        pair, _ = self._find_pair(key)
        return pair[1] if pair else None

    def hash_remove(self, key: Any) -> bool:
        """
        Remove a key-value pair from the hash table.

        Algorithm:
        1. Use _find_pair to locate the key and its bucket.
        2. If found, remove the pair from the bucket list.
        3. Return True if removed, False if the key was not found.

        Time Complexity: O(M) where M is the bucket size.
        Average Case: O(1)
        Worst Case: O(N)
        """
        pair, bucket = self._find_pair(key)
        if pair:
            bucket.remove(pair)
            return True
        return False
