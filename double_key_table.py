from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table stores data in a two-level hash table. The first key `K1` hashes
    into an outer table which contains multiple inner tables (or sub-tables). The second key `K2` then hashes
    into one of these inner tables.

    - The outer table and inner tables are implemented using open addressing with linear probing.
    - The outer table contains keys of type `K1` and values which are instances of the inner tables (LinearProbeTable).
    - The inner tables contain keys of type `K2` and values of type `V`.

    Type Arguments:
    - K1:   1st Key Type. In most cases should be string.
            Otherwise `hash1` should be overwritten.
    - K2:   2nd Key Type. In most cases should be string.
            Otherwise `hash2` should be overwritten.
    - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Initialise the DoubleKeyTable with given sizes or defaults.

        Args:
        - sizes (List[int], optional): Sizes for the external tables. Defaults to predefined TABLE_SIZES.
        - internal_sizes (List[int], optional): Sizes for the internal tables. Defaults to predefined TABLE_SIZES.

        Complexity:
        - Best and Worst: O(n), where n is the initial size of the outer table due to the initialisation of ArrayR.
          All other operations are typically O(1) average time.
        """

        if sizes is not None:
            self.external_table_sizes = sizes
        else:
            self.external_table_sizes = self.TABLE_SIZES

        if internal_sizes is not None:
            self.internal_table_sizes = internal_sizes
        else:
            self.internal_table_sizes = self.TABLE_SIZES

        self.size_index = 0

        self.external_table_array = ArrayR(self.external_table_sizes[self.size_index])

        self.external_table_length = 0


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Determine the correct position for keys using linear probing.

        Args:
        - key1 (K1): The primary key.
        - key2 (K2): The secondary key.
        - is_insert (bool): A flag indicating whether the operation is for insertion.

        Returns:
        - tuple: A tuple containing positions in the outer and inner tables.

        Raises:
        - KeyError: If the key pair doesn't exist in the table and is_insert is False.
        - FullError: If the table is full during an insertion operation.

        Complexity:
        - Best: O(1), if the initial hashed position is available or if the key exists at the initial hashed position.
        - Worst: O(n + m), where n is the size of the outer table, as we might need to probe through all slots and
          m is the inner table size (size of inner LinearProbeTable)
        """

        top_table_position = self.hash1(key1)

        for _ in range(len(self.external_table_array)):
            current_table_entry = self.external_table_array[top_table_position]

            if current_table_entry is None:
                if is_insert:
                    new_table = LinearProbeTable(self.internal_table_sizes)
                    new_table.hash = lambda k, table=new_table: self.hash2(k, table)
                    self.external_table_array[top_table_position] = (key1, new_table)

                    bottom_level_position = new_table._linear_probe(key2, True)
                    self.external_table_length += 1
                    return top_table_position, bottom_level_position
                else:
                    raise KeyError(key1, key2)

            elif current_table_entry[0] == key1:
                bottom_level_table = current_table_entry[1]

                if key2 in bottom_level_table:
                    bottom_level_position = bottom_level_table._linear_probe(key2, False)
                    return top_table_position, bottom_level_position

                else:
                    if is_insert:
                        bottom_level_position = bottom_level_table._linear_probe(key2, True)
                        return top_table_position, bottom_level_position
                    else:
                        raise KeyError(key1, key2)

            else:
                top_table_position = (top_table_position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1, key2)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        Generate an iterator (generator is a special type of iterator) over
        keys in the table.
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Args:
        - key (K1, optional): If specified, yields keys from the inner table corresponding to this key.
        Otherwise, yields all top-level keys.

        Returns/Yields:
        - A generator object of K1 | K2: Keys from the table.

        Complexity for yielding and returning a generator:
        Both best and worst case is O(1)

        Overall/Total Complexity for yielding all keys:
        - Best: O(n), if we are iterating over top-level keys and no probing is needed.
        - Worst: O(n*m), where n is the size of the outer table and m is the maximum size of an inner table.
        """
        if key is None:
            # Yield top-level keys
            for item in self.external_table_array:
                if item is not None:
                    yield item[0]
        else:
            # Yield keys from the internal hash table corresponding to the provided top-level key
            key_hash = self.hash1(key)
            key_position_outer_table = -1
            for i in range(key_hash, len(self.external_table_array)):
                if self.external_table_array[i] is not None and self.external_table_array[i][0] == key:
                    key_position_outer_table = i
                    break

            if key_position_outer_table == -1:
                raise KeyError(f"Top-level key '{key}' not found in the table.")
            else:
                for k in self.external_table_array[key_position_outer_table][1].keys():
                    yield k

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        Returns all key pairs in the hash table.

        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Args:
        - key (K1, optional): If specified, returns keys from the inner table corresponding to this key.
        Otherwise, returns all top-level keys.

        Returns:
        - list: A list of keys.

        Complexity:
        Best: O(n) where n is the size of the outer table. This happens if we are returning top-level
        keys and no probing is needed.
        Worst: O(n*m) where n is the size of the outer table and m is the maximum size of an inner table,
        and we are returning all the keys pairs and lots of probing is needed for the outer table.
        """
        if key is None:
            top_level_keys = []

            for i in range(self.table_size):
                if self.external_table_array[i] is not None:
                    top_level_keys.append(self.external_table_array[i][0])
            return top_level_keys
        else:
            key_hash = self.hash1(key)
            key_position_outer_table = -1
            for i in range(key_hash, len(self.external_table_array)):
                if self.external_table_array[i] is not None:
                    if self.external_table_array[i][0] == key:
                        key_position_outer_table = i
                        break

            if key_position_outer_table == -1:
                raise KeyError(f"Top-level key '{key}' not found in the table.")
            else:
                bottom_level_keys = self.external_table_array[key_position_outer_table][1].keys()
                return bottom_level_keys

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        Generate an iterator (generator is a special type of iterator) over
        values in the table.

        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Args:
        - key (K1, optional): If specified, yields values from the inner table corresponding to this key.
        Otherwise, yields all values.

        Returns/Yields:
        - V: Values from the table.

        Complexity for yielding and returning a generator:
        Both best and worst case is O(1)

        Total complexity to yield all values:
        Best: O(m), if we are returning values from an inner table and no probing is needed for the outer table,
        where m is the maximum size of an inner table.
        Worst: O(n*m), where n is the size of the outer table and m is the maximum size of an inner table. This
        happens when we are returning all the values in the Double Key Hash Table.
        """
        if key is None:
            # Yield all values from all internal hash tables
            for item in self.external_table_array:
                if item is not None:
                    for v in item[1].values():
                        yield v
        else:
            # Yield values from the internal hash table corresponding to the provided top-level key
            key_hash = self.hash1(key)
            key_position_outer_table = -1
            for i in range(key_hash, len(self.external_table_array)):
                if self.external_table_array[i] is not None and self.external_table_array[i][0] == key:
                    key_position_outer_table = i
                    break

            if key_position_outer_table == -1:
                raise KeyError(f"Top-level key '{key}' not found in the table.")
            else:
                for v in self.external_table_array[key_position_outer_table][1].values():
                    yield v

    def values(self, key: K1 | None = None) -> list[V]:
        """
        Return a list of values from the table.

        Args:
        - key (K1, optional): If specified, returns values from the inner table corresponding to this key.
        Otherwise, returns all values.

        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Returns:
        - list: A list of values.

        Best: O(m), if we are returning values from an inner table and no probing is needed for the outer table,
        where m is the maximum size of an inner table.
        Worst: O(n*m), where n is the size of the outer table and m is the maximum size of an inner table. This
        happens when we are returning all the values in the Double Key Hash Table.
        """
        if key is None:
            all_values = []
            for i in range(self.table_size):
                if self.external_table_array[i] is not None:
                    all_values += self.external_table_array[i][1].values()
            return all_values


        else:
            key_hash = self.hash1(key)
            key_position_outer_table = -1
            for i in range(key_hash, len(self.external_table_array)):
                if self.external_table_array[i] is not None:
                    if self.external_table_array[i][0] == key:
                        key_position_outer_table = i
                        break

            if key_position_outer_table == -1:
                raise KeyError(f"Top-level key '{key}' not found in the table.")
            else:
                bottom_level_values = self.external_table_array[key_position_outer_table][1].values()
                return bottom_level_values

    # correct
    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks if the given key pair exists in the hash table.

        Parameters:
        key (tuple): A tuple containing the two keys.

        Returns:
        bool: True if the key pair exists, otherwise False.

        Complexity:
        Best: O(1) if the key immediately resolves to a value.
        Worst: O(n + m) where n is the size of the outer table and m is the size of the inner table.
        This happens when we have to probe to the end of the outer table and then to the end of inner
        table while probing over all the elements in the inner table.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Retrieve the value associated with the given key pair.

        Parameters:
        key (tuple): A tuple containing the two keys.

        Returns:
        V: The associated value.

        Raises:
        KeyError: When the key pair is not present.

        Complexity:
        Best: O(1) when both keys immediately resolve to a value without collisions.
        Worst: O(n + m) where n is the size of the outer table and m is the size of the inner table.
        This happens when we have to probe to the end of the outer table and then to the end of inner table while
        probing over all the elements in the inner table.
        """
        top_level_key, bottom_level_key = key
        top_level_position, bottom_table_position = self._linear_probe(top_level_key, bottom_level_key, False)
        item = (self.external_table_array[top_level_position][1])[bottom_level_key]

        return item

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Insert or update a value in the Double Key hash table for a given key pair.

        Parameters:
        key: A tuple containing the two keys.
        value: The value to be set.

        Complexity
        Best: O(1) when both keys immediately resolve to an empty slot without collisions.
        Worst: O(n + m) in the worst case, potentially followed by a rehash operation, where
        n is the size of the outer table and m is the size of the inner table.
        This happens when we have to probe to the end of the outer table and then to the end of inner
        table while probing over all the elements in the inner table.
        """

        top_key, bottom_key = key
        top_level_position, bottom_level_position = self._linear_probe(top_key, bottom_key, True)

        (self.external_table_array[top_level_position][1])[bottom_key] = data

        if self.external_table_length > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Remove a value from the hash table for a given key pair.

        Parameters:
        key: A tuple containing the two keys.

        Raises:
        KeyError: When the key pair is not present.

        Complexity
        Best: O(1) when both keys immediately resolve to the item without collisions and no shuffling
        of elements is needed i.e. the next position after the deleted element is None.
        Worst: O(n + m) where m is the size of the outer table and m is the size of the inner table.
        And also we have to shuffle the elements until None is found.
        """

        top_table_key, bottom_table_key = key
        top_table_position, bottom_table_position = self._linear_probe(top_table_key, bottom_table_key, False)

        # Ensure the key exists before deletion
        if (top_table_key, bottom_table_key) not in self:
            raise KeyError(f"Key pair {key} doesn't exist in the table.")

        # Delete the key from the inner hash table
        del self.external_table_array[top_table_position][1][bottom_table_key]

        # If the inner hash table is empty after deletion, set its entry in the outer table to None
        if not self.external_table_array[top_table_position][1]:
            self.external_table_array[top_table_position] = None
            self.external_table_length -= 1

            # Start moving over the cluster
            top_table_position = (top_table_position + 1) % self.table_size
            while self.external_table_array[top_table_position] is not None:
                key2, value = self.external_table_array[top_table_position]
                self.external_table_array[top_table_position] = None
                # Reinsert
                newpos = self._linear_probe_upper_table(key2)
                self.external_table_array[newpos] = (key2, value)
                top_table_position = (top_table_position + 1) % self.table_size

    def _rehash(self) -> None:
        """
        COPIED FROM LinearProbeTable class
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """

        old_upper_table = self.external_table_array
        self.size_index += 1

        if self.size_index == len(self.external_table_sizes):
            # Cannot be resized further.
            return

        # Create a new table with the updated size
        new_size = self.external_table_sizes[self.size_index]
        self.external_table_array = ArrayR(new_size)

        for entry in old_upper_table:
            if entry is not None:
                key, internal_table = entry
                newpos = self._linear_probe_upper_table(key)
                self.external_table_array[newpos] = (key, internal_table)

    def _linear_probe_upper_table(self, key) -> int:
        """
        COPIED FROM given LinearProbeTable class
        Find the correct position for this key in the hash table using linear probing.
        :complexity best: O(hash(key)) first position is empty
        :complexity worst: O(hash(key) + N*comp(K)) when we've searched the entire table
                        where N is the tablesize
        :raises FullError: When a table is full and cannot be inserted.
        """

        position = self.hash1(key)
        start_position = position  # keep track of where we started

        while True:
            if self.external_table_array[position] is None:
                # Empty spot. Am I inserting or retrieving?
                return position

            position = (position + 1) % self.table_size  # Linearly probe to the next spot

            # Check if we've looped all the way back to the starting point
            if position == start_position:
                raise FullError("Table is full and cannot be inserted.")

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Returns:
        int: The size of the outer table.

        Complexity
        Both Best and Worst case are both O(1) as we are just returning a numeric
        value.
        """
        return len(self.external_table_array)

    def __len__(self) -> int:
        """
        Returns the number of items (key-value pairs) in the hash table.

        Returns:
        int: Total number of items in the table.

        Complexity:
        Both best and worst case is O(n*m) where n is the size of the outer table and
        m is the maximum size of the inner tables.
        """
        count = 0
        for entry in self.external_table_array:
            if entry is not None:
                count += len(entry[1])
        return count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
