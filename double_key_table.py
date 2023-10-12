from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        
        if sizes is not None:

            self.TABLE_SIZES = sizes
        
        self.size_index = 0

        self.outer_table: ArrayR[tuple[K1, V]] = ArrayR(self.TABLE_SIZES[self.size_index])

        self.count = 0

        self.size_index = 0

        self.inner_table = {}

        if internal_sizes is not None:

            self.TABLE_SIZES = internal_sizes

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
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """

        # Initial position
        position_outer_table = self.hash1(key1)

        for _ in range(self.table_size):
            if self.outer_table[position_outer_table] is None:

                if not is_insert:
                    raise KeyError(f'Error, the key pair of ({key1}, {key2}) was not found. Please try again.')

                inner_table = LinearProbeTable(self.TABLE_SIZES)

                inner_table.hash = lambda k: self.hash2(k, self.outer_table)

                self.outer_table[position_outer_table] = (key1, inner_table)

                position_inner_table = inner_table._linear_probe(key2, is_insert)

                return position_outer_table, position_inner_table

                
            elif self.outer_table[position_outer_table][0] == key1:

                inner_table = self.outer_table[position_outer_table][1]
                
                position_inner_table = self.outer_table[position_outer_table][1]._linear_probe(key2, True)

                return position_outer_table, position_inner_table
            
            else:
                # Taken by something else. Time to linear probe.
                position_outer_table = (position_outer_table + 1) % self.table_size

        if is_insert:

            raise FullError("Table is full!")
        
        else:

            raise KeyError(f'Error, the key pair of ({key1}, {key2}) was not found. Please try again.')

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for item in self.outer_table:
                if item is not None:
                    yield item[0]
        else:
            inner_table = self.outer_table[self.hash1(key)]
            if inner_table is not None:
                yield from inner_table[1].keys()

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """

        res = []
        if key is None:
            for item in self.outer_table:
                if item is not None:
                    res.append(item[0])
        else:
            inner_table = self.outer_table[self.hash1(key)]
            if inner_table is not None:
                res.extend(inner_table[1].keys())
        return res

        # res = []
        # p1, p2 = self._linear_probe(key[0], key[1], False)

        # if key is None:

        #     for _ in range(len(self.outer_table)):
        #         res.append(key[0])

        # else:
        
        #     inner_table = inner_table = self.outer_table[p1][1]

        #     for _ in range(len(inner_table)):

        #         res.append(key[1])

        # return res

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """

        key_values = self.keys(key)

        for key_value in key_values:
            if key_value is None:
                yield key_value
            else:
                inner_table = self.inner_tables.get(key_value, None)
                if inner_table is not None:
                    for item in inner_table:
                        if item is not None:
                            yield item[1]

        # key_values = self.keys(key)

        # for _ in range(key_values):

        #     if key_values is None:

        #         yield self.values
            
        #     else:

        #         inner_table = LinearProbeTable()

        #         #CHECK!!!
        #         yield inner_table[key[1]]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """

        res = []

        if key is None:
            for item in self.outer_table:
                if item is not None:
                    inner_table = item[1]
                    if inner_table is not None:
                        for inner_item in inner_table:
                            if inner_item is not None:
                                res.append(inner_item[1])
        else:
            inner_table = self.inner_tables.get(key, None)
            if inner_table is not None:
                for item in inner_table:
                    if item is not None:
                        res.append(item[1])
                        
        return res

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]

        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        p1, p2 = self._linear_probe(key[0], key[1], False)

        inner_table = self.outer_table[p1][1]

        return inner_table[key[1]]
        

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        try:

            p1, p2 = self._linear_probe(key[0], key[1], True)

            inner_table = self.outer_table[p1][1]

            inner_table[key[1]] = data

        except KeyError:

            self._rehash()
            self.__setitem__(key, data)

        else:

            if self.outer_table[p1] is None:
                
                self.count += 1

            self.outer_table[p1] = (key, data)


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        
        p1, p2 = self._linear_probe(key[0], key[1], False)

        self.outer_table[p1] = None
        self.count -= 1

        inner_table = self.outer_table[p1][1]

        p2 = (p2 + 1) % self.table_size

        while self.outer_table[p1][1] is not None:

            key[1], value = inner_table

            self.outer_table[p1][1] = None

            p2_new = self._linear_probe(key[1], True)

            inner_table[p2_new] = (key[1], value)

            p2 = (p2 + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """

        if len(self.top_level_table) > 0.5 * len(self.array):
            self.size_index += 1
            new_table_size = self.TABLE_SIZES[self.size_index]

            new_top_level_table = {}

            for key1, top_level_index in self.top_level_table.items():
                new_top_level_index = self.hash1(key1) % new_table_size
                new_top_level_table[key1] = new_top_level_index

            self.top_level_table = new_top_level_table
            self.array = ArrayR(new_table_size)

        for top_level_index, internal_table in enumerate(self.internal_tables):
            if len(internal_table) > 0.5 * len(internal_table.array):
                new_internal_table_size = self.TABLE_SIZES[self.size_index]

                new_internal_table = LinearProbeTable[K2, V](new_internal_table_size)

                for key2, value in internal_table.items():
                    new_low_level_index = self.hash2(key2, new_internal_table)
                    new_internal_table[new_low_level_index] = (key2, value)
                
                self.internal_tables[top_level_index] = new_internal_table

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        
        return len(self.outer_table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
