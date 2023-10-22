from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from data_structures import linked_stack, stack_adt

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""

        return TrailSeries(self.following.store.mountain, following = Trail(None))

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """

        self.mountain = None

        return TrailSeries(self.mountain, following = self.following)
        
    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """

        return TrailSeries(mountain, following = Trail(self))

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """

        return TrailSplit(top = Trail(None), bottom = Trail(None), following = Trail(self))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, following = self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """

        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        
        return Trail(TrailSplit(top = Trail(None), bottom = Trail(None), following = Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:

        """
        Task Implemented By: Shubh Bajpai
        
        Follow a path and add mountains according to a personality.

        This method ensures that the WalkerPersonality traverses through a trail, making decisions based on the provided. 
        The personality selects branches at splits, and mountains are added to the personality as they are encountered along the paths
        that are chosen.

        Parameters:
            personality (WalkerPersonality): The WalkerPersonality guiding the path.

        Returns:
            None

        Complexity Analysis:

        We assume that the number of elements along the path are not fixed, and contains a combination of mountains and/or trail splits,
        represented by n.

        Best Case: Based on the provided logic, the best case complexity will be O(1) when the PersonalityDecision class returns STOP for a given trail
        of size n. 

        Examples:

        Worst Case: Based on the analysis given below for all the individual functions, the worst case complexity of this function is O(n), where n is
        the number of elements along the path, including mountains and trail splits. This is because the method iterates through the entire path, 
        adding mountains to the personality. The worst-case complexity accounts that the personality decision-making is constant time.

        Examples:


        """

        from personality import PersonalityDecision

        #st
        store = self.store

        before_splitting = linked_stack.LinkedStack()

        # Complexity: O(n) (where 'n' is the number of elements along the path)
        while True:

            # Complexity: O(1)
            if store is None:
                if before_splitting.is_empty():
                    break
                # Complexity: O(1)
                store = before_splitting.pop()

            # Complexity: O(1)
            if isinstance(store, TrailSeries):
                # Complexity: O(1)
                personality.add_mountain(store.mountain)
                # Complexity: O(1)
                store = store.following.store

            # Complexity: O(1)
            elif isinstance(store, TrailSplit):
                # Complexity: O(1)
                personality_decision = personality.select_branch(Trail(store.top.store), Trail(store.bottom.store))
                # Complexity: O(1)
                before_splitting.push(store.following.store)
                top_branch = store.top
                bottom_branch = store.bottom

                # Complexity: O(1)
                if personality_decision == PersonalityDecision.TOP:
                    # Complexity: O(1)
                    store = top_branch.store
                # Complexity: O(1)
                elif personality_decision == PersonalityDecision.BOTTOM:
                    # Complexity: O(1)
                    store = bottom_branch.store
                # Complexity: O(1)
                elif personality_decision == PersonalityDecision.STOP:
                    # Complexity: O(1)
                    break

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""

        mountains_list = []  # Initialize a list to store the mountains
        stack = linked_stack.LinkedStack()  # Create a stack to traverse the trail
        stack.push(self.store)  # Start from the root of the trail

        while not stack.is_empty():  # Continue until the stack is empty
            item = stack.pop()  # Pop the top item from the stack
            if isinstance(item, TrailSeries):
                # If the item is a TrailSeries, add its mountain to the list
                mountains_list.append(item.mountain)
                # Push the following trail onto the stack for further exploration
                stack.push(item.following.store)
            elif isinstance(item, TrailSplit):
                # If the item is a TrailSplit, push the top and bottom branches
                stack.push(item.top.store)
                stack.push(item.bottom.store)
                # Push the following trail onto the stack for further exploration
                stack.push(item.following.store)

        return mountains_list  # Return the list of mountains

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]:
        """Calculates paths through the trail with a maximum difficulty level."""

        all_store_paths = []  # Initialize a list to store all valid paths
        ind_path = []  # Initialize an individual path list
        follow_path_list = []  # Initialize a list for tracking the following paths
        self.difficulty_maximum_auxiliary(self.store, max_difficulty, all_store_paths, ind_path, follow_path_list)
        return all_store_paths  # Return the list of paths

    def difficulty_maximum_auxiliary(self, current_store: TrailStore, max_difficulty, all_store_paths, ind_path, follow_path_list):
        """Auxiliary function to calculate paths with a maximum difficulty level."""

        if isinstance(current_store, TrailSplit):
            # If the current store is a TrailSplit, explore both top and bottom branches
            self.difficulty_maximum_auxiliary(current_store.top.store, max_difficulty, all_store_paths, ind_path[:], follow_path_list + [current_store.following.store])
            self.difficulty_maximum_auxiliary(current_store.bottom.store, max_difficulty, all_store_paths, ind_path[:], follow_path_list + [current_store.following.store])
        elif isinstance(current_store, TrailSeries):
            # If the current store is a TrailSeries, check if the mountain's difficulty is within the limit
            if current_store.mountain.difficulty_level <= max_difficulty:
                ind_path.append(current_store.mountain)
                self.difficulty_maximum_auxiliary(current_store.following.store, max_difficulty, all_store_paths, ind_path, follow_path_list)
            else:
                ind_path.clear()
        else:
            # If the current store's following is None, we backtrack
            if not len(follow_path_list) == 0:
                current_store = follow_path_list.pop()
                self.difficulty_maximum_auxiliary(current_store, max_difficulty, all_store_paths, ind_path, follow_path_list)
            else:
                # We have reached the end of a path, add it to the list of valid paths
                all_store_paths.append(ind_path)

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()

if __name__ == "__name__":
    ...