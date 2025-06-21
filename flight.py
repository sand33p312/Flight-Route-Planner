class Flight:
    def __init__(self, flight_no, start_city, departure_time, end_city, arrival_time, fare):
        """ Class for the flights

        Args:
            flight_no (int): Unique ID of each flight
            start_city (int): The city no. where the flight starts
            departure_time (int): Time at which the flight starts
            end_city (int): The city no where the flight ends
            arrival_time (int): Time at which the flight ends
            fare (int): The cost of taking this flight
        """
        self.flight_no = flight_no
        self.start_city = start_city
        self.departure_time = departure_time
        self.end_city = end_city
        self.arrival_time = arrival_time
        self.fare = fare


"""
If there are n flights, and m cities:

1. Flight No. will be an integer in {0, 1, ... n-1}
2. Cities will be denoted by an integer in {0, 1, .... m-1}
3. Time is denoted by a non negative integer - we model time as going from t=0 to t=inf
"""

class Heap:
    '''
    Class to implement a heap with a general comparison function
    '''
    
    def __init__(self, comparison_function, init_array=None):
        # Initialize heap with a comparison function and optional initial array
        self.init_array = init_array if init_array else []
        self.comparison_function = comparison_function
        self._build_heap()
        
    def insert(self, value):
        self.init_array.append(value)
        self._upheap(len(self.init_array) - 1)
    
    def extract(self):
        if len(self.init_array) != 0:
            self._swap(0, len(self.init_array) - 1)
            min_element = self.init_array.pop()
            self._downheap(0)
            return min_element

    def top(self):
        if len(self.init_array) != 0:
            return self.init_array[0]
        
    def _parent(self, j):
        return (j - 1) // 2
    
    def _left(self, j):
        return 2 * j + 1
    
    def _right(self, j):
        return 2 * j + 2
    
    def _has_left(self, j):
        return self._left(j) < len(self.init_array)
    
    def _has_right(self, j):
        return self._right(j) < len(self.init_array)
    
    def _swap(self, i, j):
        self.init_array[i], self.init_array[j] = self.init_array[j], self.init_array[i]
    
    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self.comparison_function(self.init_array[j], self.init_array[parent]) < 0:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            smallest_child = left
            if self._has_right(j):
                right = self._right(j)
                if self.comparison_function(self.init_array[right], self.init_array[left]) < 0:
                    smallest_child = right
            if self.comparison_function(self.init_array[smallest_child], self.init_array[j]) < 0:
                self._swap(j, smallest_child)
                self._downheap(smallest_child)
    
    def _build_heap(self):
        '''To initialize the heap in O(n) time'''
        for i in range(len(self.init_array) // 2, -1, -1):
            self._downheap(i)

