from __future__ import annotations

from mountain import Mountain

from algorithms import binary_search, mergesort

class MountainOrganiser:

    def __init__(self) -> None:

        self.mountain_list = []
        self.mountain_rankings = {}
        self.mountain_count = 0

    def cur_position(self, mountain: Mountain) -> int:
        
        #complexity of the mountain_ranking is O(log(N)), where N is the total # of mountains
        mountain_ranking = binary_search.binary_search(self.mountain_list, mountain)

        if  self.mountain_list[mountain_ranking] != mountain:
            raise KeyError("Error. The mountain was not found in the list.")
        
        return mountain_ranking

    def add_mountains(self, mountains: list[Mountain]) -> None:

        sorted_mountain_list = mergesort.mergesort(mountains)
        self.mountain_list = mergesort.merge(self.mountain_list, sorted_mountain_list)