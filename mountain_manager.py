from __future__ import annotations
from mountain import Mountain
from infinite_hash_table import InfiniteHashTable
from data_structures.hash_table import LinearProbeTable


class MountainManager:
    """
    The MountainManager clas manages and organises mountains based on their characteristics such as name,
    difficulty level, and length. And also, sort and group mountains by a particular difficulty level.

    Attributes:
    mountains (LinearProbeTable): A table containing mountains identified by their names (assuming names are
    generally unique for any mountains).
    difficulty_groups (InfiniteHashTable): A table that groups mountains based on their difficulty level.

    Note:
    Both LinearProbeTable and InfiniteHashTable are assumed to have O(1) best and worst case complexities
    for their operations.
    """

    def __init__(self) -> None:
        """
        Initialises a new MountainManager with empty mountains and difficulty_groups tables.

        Complexity:
        Best Case: O(1) as we are simply creating new LinearProbeTable and InfiniteHashTable objects,
        both of which are O(1).
        Worst Case: O(1) as we are simply creating new LinearProbeTable and InfiniteHashTable objects,
        both of which are O(1).
        """
        self.mountains = LinearProbeTable()
        self.difficulty_groups = InfiniteHashTable()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adds a new mountain to the mountains table and updates the difficulty_groups table.

        Args:
        mountain (Mountain): The mountain object to be added.

        Raises:
        ValueError: If the mountain with the given name already exists.

        Complexity:
        Best Case: O(1) as setitem operation (and all other operations for LinearProbeTable and
        InfiniteHashTable) are assumed to be O(1)
        Worst Case: O(1) as setitem operation (and all other operations for LinearProbeTable and
        InfiniteHashTable) are assumed to be O(1)
        """
        mountain_name = mountain.get_name()
        mountain_difficulty_level = str(mountain.get_difficulty_level())
        mountain_length = mountain.get_length()

        if mountain_name in self.mountains:
            raise ValueError(f"Mountain with name {mountain_name} already exists!")

        self.mountains[mountain_name] = (mountain_difficulty_level, mountain_length)

        try:
            if mountain not in self.difficulty_groups[str(mountain_difficulty_level)]:
                self.difficulty_groups[str(mountain_difficulty_level)].append(mountain)
        except KeyError:
            self.difficulty_groups[str(mountain_difficulty_level)] = [mountain]

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Removes a mountain from the mountains table and updates the difficulty_groups table accordingly.

        Args:
        mountain (Mountain): The mountain object to be removed.

        Complexity:
        Best Case: O(1) as delitem operation (and all other operations for LinearProbeTable and
        InfiniteHashTable) are assumed to be O(1)
        Worst Case: O(1) as as delitem operation (and all other operations for LinearProbeTable and
        InfiniteHashTable) are assumed to be O(1)
        """
        mountain_name = mountain.get_name()
        mountain_difficulty_level = str(mountain.get_difficulty_level())
        del self.mountains[mountain_name]
        self.difficulty_groups[mountain_difficulty_level].remove(mountain)
        if not self.difficulty_groups[mountain_difficulty_level]:
            del self.difficulty_groups[mountain_difficulty_level]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Edits the details of an existing mountain. This is achieved by removing the old mountain details
        (remove the whole mountain object) and adding the new mountain details (adding a whole new mountain
        object). Since, all the operations are assumed to be O(1) for LinearProbeTable and InfiniteHashTable,
        this is still efficient and O(1).

        Args:
        old (Mountain): The old mountain object which needs to be edited.
        new (Mountain): The new mountain object with updated details.

        Complexity:
        Best Case: O(1) as the remove_mountain and add_mountain have the best case O(1)
        Worst Case: O(1) as the remove_mountain and add_mountain have the worst case O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Returns a list of mountains with the specified difficulty level.

        Args:
        diff (int): The difficulty level to filter/sort mountains by.

        Returns:
        list[Mountain]: A list of mountains with the specified difficulty level.

        Complexity:
        Best Case: O(1) as all the operations for InfiniteHashTable have the worst case O(1)
        Worst Case: O(1) as all the operation for InfiniteHashTable have the worst case O(1)
        """
        try:
            return self.difficulty_groups[str(diff)]
        except KeyError:
            return []

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Groups all the mountains by their difficulty level.

        Returns:
        list[list[Mountain]]: A nested list where each sublist contains mountains of a specific difficulty level.

        Complexity:
        Best Case: O(n*m), where n is the number of difficulty levels and m is the number of mountains with a
        particular difficulty level. The sort_keys() is O(1) by our assumption that all InfiniteHashTable operations
        are O(1)
        Worst Case: O(n*m), where n is the number of difficulty levels and m is the number of mountains with a
        particular difficulty level. The sort_keys() is O(1) by our assumption that all InfiniteHashTable operations
        are O(1)
        """
        difficulties = self.difficulty_groups.sort_keys()
        return [self.difficulty_groups[diff] for diff in difficulties if self.difficulty_groups[diff]]
