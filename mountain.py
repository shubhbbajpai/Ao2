from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    # Define the equality comparison method.
    def __eq__(self, other):
        # Check if the difficulty levels and names of two mountains are equal.
        if self.difficulty_level == other.difficulty_level:
            if self.name == other.name:
                # Return True if both mountains are equal.
                return self.name == other.name
        # Return False if any of the conditions are not met.

    # Define the less than comparison method.
    def __lt__(self, other):
        # Check if the difficulty level of self is less than the difficulty level of other.
        if self.difficulty_level < other.difficulty_level:
            return self.difficulty_level < other.difficulty_level
        # If difficulty levels are equal, check lexicographic order of names.
        elif self.difficulty_level > other.difficulty_level:
            return False
        elif self.difficulty_level == other.difficulty_level:
            return self.name < other.name

    # Define the greater than comparison method.
    def __gt__(self, other):
        # Check if the difficulty level of self is greater than the difficulty level of other.
        if self.difficulty_level > other.difficulty_level:
            return self.difficulty_level > other.difficulty_level
        # If difficulty levels are equal, check lexicographic order of names.
        elif self.difficulty_level < other.difficulty_level:
            return False
        elif self.difficulty_level == other.difficulty_level:
            return self.name > other.name

    # Define the less than or equal to comparison method.
    def __le__(self, other):
        # Check if the difficulty level of self is less than or equal to the difficulty level of other.
        if self.difficulty_level < other.difficulty_level:
            return True
        # If difficulty levels are equal, check lexicographic order of names.
        if self.difficulty_level == other.difficulty_level:
            return self.name <= other.name
        # Return False if self's difficulty level is greater than other's.

    # Define the greater than or equal to comparison method.
    def __ge__(self, other):
        # Check if the difficulty level of self is greater than or equal to the difficulty level of other.
        if self.difficulty_level > other.difficulty_level:
            return True
        # If difficulty levels are equal, check lexicographic order of names.
        if self.difficulty_level == other.difficulty_level:
            return self.name >= other.name
        # Return False if self's difficulty level is less than other's.

    def get_name(self) -> str:
        return self.name

    def get_difficulty_level(self) -> int:
        return self.difficulty_level

    def get_length(self) -> int:
        return self.length
