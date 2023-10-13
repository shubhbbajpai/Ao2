from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    #if both mountains are equal to each other.
    def __eq__(self, other):

        if self.difficulty_level == other.difficulty_level:
            if self.name == other.name:
                return self.name == other.name
        return False
    
    #if both mountains are less than to each other.
    def __lt__(self, other):
        if self.difficulty_level < other.difficulty_level:
            return self.difficulty_level < other.difficulty_level
        
        elif self.difficulty_level > other.difficulty_level:
            return False
        
        elif self.difficulty_level == other.difficulty_level:
            return self.name < other.name

    #if both mountains are greater than to each other. 
    def __gt__(self, other):
        
        if self.difficulty_level > other.difficulty_level:
            return self.difficulty_level > other.difficulty_level
        
        elif self.difficulty_level < other.difficulty_level:
            return False
        
        elif self.difficulty_level == other.difficulty_level:
            return self.name > other.name
        
    def __le__(self, other):
        if self.difficulty_level < other.difficulty_level:
            return True
        if self.difficulty_level == other.difficulty_level:
            return self.name <= other.name
        return False
        
    def __ge__(self, other):
        if self.difficulty_level > other.difficulty_level:
            return True
        if self.difficulty_level == other.difficulty_level:
            return self.name >= other.name
        return False