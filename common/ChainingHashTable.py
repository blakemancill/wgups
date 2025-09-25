class ChainingHashTable:
    def __init__(self, initial_capacity = 20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # Inserts a new item into the hash table, handling both insertion and update
    def insert(self, key, item):
        # Gets the bucket list where the item will go
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Updates key if it is already present in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # Else, inserts the item into the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Looks up an item in hash table
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None

