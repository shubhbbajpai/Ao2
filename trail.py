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
        """Follow a path and add mountains according to a personality."""
        from personality import PersonalityDecision

        store = self.store

        before_splitting = linked_stack.LinkedStack()

        while True:

            if store is None:
                
                if before_splitting.is_empty():

                    break

                store = before_splitting.pop()

            if isinstance(store, TrailSeries):

                personality.add_mountain(store.mountain)

                store = store.following.store

            elif isinstance(store, TrailSplit):

                #allows for the personality to choose between the top and bottom branch
                personality_decision = personality.select_branch(Trail(store.top.store), Trail(store.bottom.store))

                before_splitting.push(store.following.store)

                top_branch = store.top

                bottom_branch = store.bottom

                if personality_decision == PersonalityDecision.TOP:
                    
                    store = top_branch.store

                elif personality_decision == PersonalityDecision.BOTTOM:

                    store = bottom_branch.store

                elif personality_decision == PersonalityDecision.STOP:
                    
                    break

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""

        mountains_list = []
        stack = linked_stack.LinkedStack()
        stack.push(self.store)

        while not stack.is_empty():
            item = stack.pop()
            if isinstance(item, TrailSeries):
                mountains_list.append(item.mountain)
                stack.push(item.following.store)
            elif isinstance(item, TrailSplit):
                stack.push(item.top.store)
                stack.push(item.bottom.store)
                stack.push(item.following.store)

        return mountains_list

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!

        all_store_paths = []
        ind_path = [] # individual path
        follow_path_list = [] #follow list
        self.difficulty_maximum_auxilary(self.store, max_difficulty, all_store_paths, ind_path, follow_path_list) 
        return all_store_paths
    
    def difficulty_maximum_auxilary(self, current_store: TrailStore, max_difficulty, all_store_paths, ind_path, follow_path_list):

        if isinstance (current_store, TrailSplit):
            self.difficulty_maximum_auxilary (current_store.top.store, max_difficulty, all_store_paths, ind_path[:], follow_path_list+ [current_store. following.store]) 
            self.difficulty_maximum_auxilary(current_store.bottom. store, max_difficulty, all_store_paths, ind_path[:], follow_path_list+ [current_store.following.store])
        
        elif isinstance(current_store, TrailSeries):
            if current_store.mountain.difficulty_level <= max_difficulty:
                ind_path.append(current_store.mountain)
                self.difficulty_maximum_auxilary(current_store.following.store, max_difficulty, all_store_paths, ind_path, follow_path_list)
            else:
                ind_path.clear()
        else: # current store.following is None 
            if not len(follow_path_list) == 0:
                current_store = follow_path_list.pop()
                self.difficulty_maximum_auxilary(current_store, max_difficulty, all_store_paths, ind_path, follow_path_list)
            else:
                all_store_paths.append(ind_path)

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()

if __name__ == "__name__":
    ...