from __future__ import annotations

from mountain import Mountain

from algorithms import binary_search, mergesort

class MountainOrganiser:

    def __init__(self) -> None:

        """

        Implemented by: Shubh Bajpai

        This __init__ method initializes the MountainOrganiser to start organizing mountains. The variables initialized are:

             - self.mountain_list: contains the list of all the mountains arranged based either their difficulty level or name.

        Complexity Analysis:

        - Best Case: O(1)
        - Worst Case: O(1)

        """

        self.mountain_list = []

    def cur_position(self, mountain: Mountain) -> int:

        """

        This cur_position method returns the rank (position) of the given mountain in the organiser using Binary Search. Based on the provided mountain_list, we 
        perform BinarySearch and store the position of the mountain we are trying to search within the variable mountain_ranking. After, we return the 
        value of mountain_ranking.

        Parameters:
        - mountain (Mountain): The mountain to find the rank for.

        Returns:
        - int: The rank of the mountain within mountain_list.

        Raises:
        - KeyError: If the provided mountain hasn't been added yet.

        Example:

        >>>mountain_list = [m1, m3, m7, m9]
        >>>cur_position(m4)
        KeyError: Error. The mountain was not found in the list.

        Complexity Analysis:

        Based on the analysis given below for all the individual functions, the best case complexity is O(1). This is when the mountain is
        in the middle of mountain_list of size N, where N is the total number of mountains included so far.

        Based on the analysis given below for all the individual functions, the worst case complexity is O(logN), where N is the 
        total number of mountains included so far. This would occur when the position of the mountain is less than or greater than the middle.
        Since the search pool is halved each time, it will take a maximum of O(logN) comparisions in order to find the mountain. Hence, the worst 
        case occurs when it takes O(logN) comparisons to find the mountain within mountain_list.

        """
        
        #complexity of the mountain_ranking is O(log(N)), where N is the total # of mountains
        mountain_ranking = binary_search.binary_search(self.mountain_list, mountain)  # O(logN)

        if self.mountain_list[mountain_ranking] != mountain:  # O(1)

            raise KeyError("Error. The mountain was not found in the list.")  # O(1)
        
        return mountain_ranking  # O(1)

    def add_mountains(self, mountains: list[Mountain]) -> None:

        """

        This method add_mountains stores the mountains (list[Mountain]) into a new list, and conducts the mergesort() operation to sort the new list.
        Each mountain is sorted based on their difficulty level, accessed within the Mountain class. If two mountains have the same difficulty
        level, then the name of the mountains are compared together instead and sorting in lexicographical order.

        Within the Mountain class, I have defined magic methods which implement the logic to first sort the mountains based on their difficulty level,
        and then their name if need be.

        After, using the merge() operation, the new list is merged together with the existing list mountain_list to produce a new list.

        Parameters:
        - mountains (list[Mountain]): A list of Mountain objects to be added to the organiser.

        Returns:
        None

        Complexity Analysis:

        The complexity analysis is being conducted assumes that there is a large input size of 'M', where M is the length of the input list 'mountains'.
        'N' is the total number of mountains having combined the smaller lists together.

        Within mergesort(), the complexity is Mlog(M) because mergesort will divide the inputted into M sublists. This takes log(N) time, as the size of
        the inputted list is divided in half at each level of recursion. Then, the sublists are merged to produce larger sorted sublists. This merging 
        step takes O(M) time for each level of recursion.

        Within merge(), the complexity is O(N) because the length of the inputted list and the length of the existing list combine to form the total
        length of N mountains. 
        
        Based on the analysis given below for all the individual functions, the best case complexity will be O(Mlog(M) + N). This occurs when the inputted 
        list of mountains is already sorted, however, each element will still undergo comparisons. 

        Based on the analysis given below for all the individual functions, the worst case complexity will also be O(Mlog(M) + N). This occurs when the inputted 
        list of mountains is sorted in the opposite order, however, the number of operations will not grow, as the same number of operations based on the length
        of the list will be conducted.

        """

        sorted_mountain_list = mergesort.mergesort(mountains)  # O(Mlog(M))
        self.mountain_list = mergesort.merge(self.mountain_list, sorted_mountain_list)  # O(N)