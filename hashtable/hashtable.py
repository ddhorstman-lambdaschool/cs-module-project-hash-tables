class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value, next_=None):
        self.key = key
        self.value = value
        self.next = next_

    def __str__(self):
        return f"[{self.key}]: {self.value}"

    def __repr__(self):
        return f"<HashTableEntry {str(self)} >"


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity if capacity > MIN_CAPACITY else MIN_CAPACITY
        self.length = 0
        self.storage = [None] * self.capacity

    def __len__(self):
        return self.length

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join([str(i) for i in self.__retrieve_data("objects")])
            + "\n}"
        )

    def __repr__(self):
        return (
            "<HashTable\n\t"
            + "\n\t".join([repr(i) for i in self.__retrieve_data("objects")])
            + "\n>"
        )

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.put(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __iter__(self):
        self.key_cache = self.keys()
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.key_cache):
            return_val = self.key_cache[self.idx]
            self.idx += 1
            return return_val
        else:
            del self.key_cache
            del self.idx
            raise StopIteration

    def clear(self):
        self.length = 0
        self.storage = [None] * self.capacity

    def copy(self):
        ht = HashTable(self.capacity)
        for key, value in self.items():
            ht.put(key,value)
        return ht

    @staticmethod
    def fromkeys(keys, value=None):
        ht = HashTable(len(keys))
        for key in keys:
            ht.put(key,value)
        return ht

    def pop(self, key, default=None):
        try:
            return self.delete(key)
        except KeyError:
            return None

    def setdefault(self, key, value=None):
        current_value = self.get(key)
        if current_value:
            return current_value
        else:
            self.put(key, value)
            return value

    def update(self, entries):
        if type(entries) is dict:
            for key, value in entries.items():
                self.put(key, value)

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.length / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        hash = 14695981039346656037
        for byte in key.encode():
            hash *= 1099511628211
            hash ^= byte
        return hash

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for byte in key.encode():
            hash = ((hash << 5) + hash) + byte
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        idx = self.hash_index(key)
        entry = self.storage[idx]
        # If the slot is empty, initialize it with this new entry
        if not entry:
            self.storage[idx] = HashTableEntry(key, value)
            self.length += 1

        else:
            while True:
                # If the key is in the table, change its value
                if entry.key == key:
                    entry.value = value
                    return

                entry = entry.next
                # If key not in table, create a new entry
                if entry is None:
                    new_entry = HashTableEntry(key, value, self.storage[idx])
                    self.storage[idx] = new_entry
                    self.length += 1
                    break

        # Auto-resize if necessary
        if(self.get_load_factor() > 0.7):
            self.resize(self.capacity * 2)

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        idx = self.hash_index(key)
        entry = self.storage[idx]
        return_val = None

        if entry is None:
            raise KeyError(key)

        # Special case: entry is the head of the LinkedList
        if entry.key == key:
            self.storage[idx] = entry.next
            self.length -= 1
            return_val = entry.value

        else:
            while entry.next is not None:
                # If the next item is the target,
                # cut it out of the list
                if entry.next.key == key:
                    return_val = entry.next.value
                    entry.next = entry.next.next
                    self.length -= 1
                    break

                entry = entry.next
            # If we made it thru the list without finding it
            else:
                raise KeyError(key)

        # Auto-resize if necessary
        if(self.get_load_factor() < 0.2):
            self.resize(self.capacity//2)

        return return_val

    def get(self, key, default=None):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        idx = self.hash_index(key)
        entry = self.storage[idx]

        if not entry:
            return default

        while True:
            if entry.key == key:
                return entry.value
            entry = entry.next
            if entry is None:
                return default

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        if new_capacity < MIN_CAPACITY:
            new_capacity = MIN_CAPACITY

        old_items = self.items()

        self.capacity = new_capacity
        self.storage = [None] * self.capacity
        self.length = 0

        for key, value in old_items:
            self.put(key, value)

    def items(self):
        return self.__retrieve_data("both")

    def keys(self):
        return self.__retrieve_data("keys")

    def values(self):
        return self.__retrieve_data("values")

    def __retrieve_data(self, mode):
        if mode not in ["both", "keys", "values", "objects"]:
            print("Invalid mode for this function")
            return

        data = [None] * self.length
        idx = 0

        # Loop through each index
        for entry in self.storage:
            if entry is None:
                continue

            # Loop though each LinkedList item
            while True:
                data[idx] = self.__filter_data(entry, mode)
                idx += 1
                entry = entry.next
                if entry is None:
                    break
        return data

    def __filter_data(self, entry, mode):
        if mode == "both":
            return (entry.key, entry.value)
        elif mode == "keys":
            return entry.key
        elif mode == "values":
            return entry.value
        elif mode == "objects":
            return entry


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    ht["new_entry"] = "hello"
    print(ht["new_entry"])

    for key in ht:
        print(ht[key])

    del ht["new_entry"]

    # Test storing beyond capacity
    # for i in range(1, 13):
    #     print(ht.get(f"line_{i}"))

    # # Test resizing
    # old_capacity = ht.get_num_slots()
    # ht.resize(ht.capacity * 2)
    # new_capacity = ht.get_num_slots()

    # print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # # Test if data intact after resizing
    # for i in range(1, 13):
    #     print(ht.get(f"line_{i}"))

    print("")
