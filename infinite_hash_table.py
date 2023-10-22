from typing import Generic, TypeVar
from algorithms.mergesort import mergesort
from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    A hash table implementation that can infinitely nest tables based on key length.

    Attributes:
    - TABLE_SIZE: An integer constant representing the size of the hash table.
    - level: The depth level of the current hash table in the nested structure.
    - table: The actual storage array of the hash table.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        """
        Initialise an InfiniteHashTable.

        Parameters:
        - level (int): The depth level for the table. Defaults to 0 for the topmost table.

        Complexity:
        Best and Worst case are both O(n) where n is the size/length of the ArrayR in general cases
        """
        self.level = level
        self.table = ArrayR(self.TABLE_SIZE)

    def hash(self, key: K) -> int:
        """
        Compute the hash index for the given key based on its character at the current table's level.

        Parameters:
        - key (K): The key to hash.

        Returns:
        int: The hash index.

        Complexity:
        Best and Worst case are both O(1) as only one character of the key is used for hashing.
        """
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
       Retrieve the value associated with the given key.

       Parameters:
       - key (K): The key for the lookup.

       Returns:
       V: The value associated with the key.

       Complexity:
       Best Case: O(1), if the key is found at the current table level
       Worst Case: O(d), where d is the depth of nested tables for the key
       """
        index = self.hash(key)
        entry = self.table[index]

        if isinstance(entry, InfiniteHashTable):
            return entry[key]
        if entry and entry[0] == key:
            return entry[1]
        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set the value for the given key in the hash table.

        Parameters:
        - key (K): The key for the value.
        - value (V): The value to set.

        Complexity:
        Best Case: O(1), if a position is directly available, or we are overwriting
        Worst Case: O(d), where d is the depth of nested tables for the key and
        if we need to go d levels deep to set the value
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            self.table[index] = (key, value)
            return
        if isinstance(entry, InfiniteHashTable):
            entry[key] = value
            return
        if entry[0] == key:
            self.table[index] = (key, value)
            return

        sub_table = InfiniteHashTable(self.level + 1)
        sub_table[entry[0]] = entry[1]
        sub_table[key] = value
        self.table[index] = sub_table

    def __delitem__(self, key: K) -> None:
        """
        Delete the key-value pair for the given key from the hash table.

        Parameters:
        - key (K): The key to delete.

        Complexity:
        Best Case: O(1), if the key is found at the initial table level 0
        Worst Case: O(d), where d is the depth of nested tables for the key
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            raise KeyError(key)

        # If it's a nested-table, delegate the deletion to it.
        if isinstance(entry, InfiniteHashTable):
            del entry[key]
            # After deleting, if the nested-table has only one item left, elevate that item.
            if len(entry) == 1:
                k, v = next(iter(entry.items()))
                self.table[index] = (k, v)
            # If it's empty, set the slot to None.
            elif len(entry) == 0:
                self.table[index] = None
            return

        # If it's a key-value pair, delete if the key matches.
        if entry[0] == key:
            self.table[index] = None
            return

        raise KeyError(key)

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the hash table.

        Returns:
        int: The number of key-value pairs.

        Complexity:
        Best Case: O(TABLE_SIZE), when there are no nested tables and all the keys are at level 0
        Worst Case: O(TABLE_SIZE * d), where d is the depth of nested tables
        """
        count = 0
        for item in self.table:
            if item is None:
                continue
            # If the item is another hash table, recursively count its items
            if isinstance(item, InfiniteHashTable):
                count += len(item)
            # If the item is a value, increment the count
            else:
                count += 1
        return count

    def get_location(self, key: K) -> list[int]:
        """
        Get the sequence of indices leading to the given key in the nested tables.

        Parameters:
        - key (K): The key to find.

        Returns:
        list[int]: List of indices showing the path to the key.

        Complexity:
        Best Case: O(1), if the key is found at the initial table level 0
        Worst Case: O(d), where d is the depth of nested tables for the key
        """
        index = self.hash(key)
        entry = self.table[index]

        if entry is None:
            raise KeyError(key)
        if isinstance(entry, InfiniteHashTable):
            return [index] + entry.get_location(key)
        if entry[0] == key:
            return [index]
        raise KeyError(key)

    def sort_keys(self) -> list[str]:
        """
        Returns a list of keys sorted in lexicographical order using mergesort.

        Returns:
        List[str]: Sorted keys.

        Complexity:

        Best Case: O(n*log(n)) - Due to the sorting operation by mergesort which has complexity
        of O(n*log(n)) and n is the number of items/keys in the infinite hash table. The best-case
        scenario would occur when all keys are present at the level 0 with no nested hash tables.

        Worst Case: O(n*log(n)) - Due to the sorting operation by mergesort which has complexity
        of O(n*log(n)) and n is the number items/keys in the infinite hash table.
        In the worst-case scenario, the keys can be distributed evenly across all nested hash tables
        up to a depth of d. The sort_keys function would be called recursively d times for each nested
        table. However, the way mergesort works, sorting the keys at each level doesn't stack
        multiplicatively with depth, since the keys are partitioned and then combined. The worst-case
        complexity will then be O(d*n + n*logn). But, Since nlogn will grow faster than d×n for a large n,
        the nlogn term dominates and hence the worst case complexity.
        """
        keys = []
        for i, entry in enumerate(self.table):
            if isinstance(entry, InfiniteHashTable):
                keys.extend(entry.sort_keys())
            elif entry:
                keys.append(entry[0])
        return mergesort(keys)

    def items(self) -> list[tuple[K, V]]:
        """
        Get all key-value pairs in the hash table.

        Returns:
        list[tuple[K, V]]: List of key-value pairs.

        Complexity:
        Best Case: O(TABLE_SIZE), if the key is always found at the initial level i.e. level 0
        and there are no nested-tables
        Worst Case: O(TABLE_SIZE * d) where d is the depth of nested tables
        """
        result = []
        for entry in self.table:
            if isinstance(entry, InfiniteHashTable):
                result.extend(entry.items())
            elif entry:
                result.append(entry)
        return result
