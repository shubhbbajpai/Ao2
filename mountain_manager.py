from __future__ import annotations
from mountain import Mountain

from data_structures import hash_table

class MountainManager:

    def __init__(self) -> None:
        
        self.mountain_organized = hash_table.LinearProbeTable()

    def add_mountain(self, mountain: Mountain) -> None:
        table[(k1,k2)]
        self.mountain_organized.hash

    def remove_mountain(self, mountain: Mountain) -> None:
        
        self.mountain_organized.pop(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        
        ...

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        raise NotImplementedError()

    def group_by_difficulty(self) -> list[list[Mountain]]:
        raise NotImplementedError()
