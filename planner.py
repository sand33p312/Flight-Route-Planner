from flight import Flight,Heap

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights

        self.max_start_city = max(flight.end_city for flight in self.flights) + 1 # find max of start_city no.
        
        self.cities = None  # initialisation each flight destination.

        for flight in flights:
            flight.neighbour_list = []

        self.set_cities()

        for flight in flights:
            for neighbour_flight in self.cities[flight.end_city].destinations:
                if flight.arrival_time+20 <= neighbour_flight.departure_time:
                    flight.neighbour_list.append(neighbour_flight)

        
    def set_cities(self):
        self.cities = [Node() for _ in range(self.max_start_city)]
        for flight in self.flights:
            self.cities[flight.start_city].destinations.append(flight)
    
        # Reset visited status, best_path, and total_cost for all nodes
        for city in self.cities:
            city.visited = False
            city.best_path = []
            city.total_cost = float('inf')

    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        self.set_cities()

        queue = Queue()
        queue.enqueue((start_city, t1))

        best_route = None

        while not queue.isEmpty():
            current_city, current_time = queue.dequeue()

            if current_city == end_city:
                if best_route is None or len(self.cities[current_city].best_path) < len(best_route) or (
                    len(self.cities[current_city].best_path) == len(best_route) and 
                    self.cities[current_city].best_path[-1].arrival_time < best_route[-1].arrival_time
                ):
                    best_route = self.cities[current_city].best_path
                continue

            for flight in self.cities[current_city].destinations:
                end_city_node = self.cities[flight.end_city]

                if flight.departure_time >= current_time + (20 if current_city != start_city else 0) and flight.arrival_time <= t2:
                    new_path = self.cities[current_city].best_path + [flight]

                    if not end_city_node.visited or len(new_path) < len(end_city_node.best_path) or (
                        len(new_path) == len(end_city_node.best_path) and 
                        flight.arrival_time < end_city_node.best_path[-1].arrival_time
                    ):
                        end_city_node.best_path = new_path
                        end_city_node.visited = True
                        queue.enqueue((flight.end_city, flight.arrival_time))

        return best_route if best_route else []  

    def _fare_comparison(self, a, b):
        """Comparison function for the min-heap based on fare."""
        return a[0] - b[0]
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        min_heap = Heap(self._fare_comparison)

        min_cost_to_city = [float('inf') for _ in range(len(self.flights))]

        # Insert initial flights starting from start_city that satisfy the time constraint
        for flight in self.flights:
            if flight.start_city == start_city and flight.departure_time >= t1 and flight.arrival_time <= t2:
                min_heap.insert((flight.fare, flight, [flight]))
                if min_cost_to_city[flight.flight_no] > flight.fare:
                    min_cost_to_city[flight.flight_no] = flight.fare

        best_route = None
        min_cost = float('inf')

        while len(min_heap.init_array) > 0:
            current_cost, current_flight, current_path = min_heap.extract()

            # If destination is reached, update best_route if this route is cheaper
            if current_flight.end_city == end_city:
                if current_cost < min_cost:
                    best_route = current_path
                    min_cost = current_cost
                continue

            for next_flight in current_flight.neighbour_list:
                if next_flight.arrival_time <= t2:
                    new_cost = current_cost + next_flight.fare

                    # Only consider this path if its cheaper than any previously found path to next_flight.end_city
                    if new_cost < min_cost_to_city[next_flight.flight_no]:
                        min_cost_to_city[next_flight.flight_no] = new_cost
                        new_path = current_path + [next_flight]
                        min_heap.insert((new_cost, next_flight, new_path))

        return best_route if best_route else []

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
            """
            Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
            arrives before t2 (<=) satisfying:
            The route has the least number of flights, and within routes with the same number of flights,
            is the cheapest.
            """
            heap = Heap(self._fare_comparison)
            
            heap.insert((0, 0, start_city, t1, []))  # (hops, cost, current_city, current_time, path)
            
            best_route = None
            
            for flight in self.flights:
                flight.best_hops = float('inf')
                flight.best_cost = float('inf')

            while heap.top():
                hops, cost, current_city, current_time, path = heap.extract()

                if current_city == end_city:
                    if best_route is None or len(path) < len(best_route) or (
                        len(path) == len(best_route) and cost < sum(f.fare for f in best_route)
                    ):
                        best_route = path
                    continue

                current_city_node = self.cities[current_city]
                
                for flight in current_city_node.destinations:
                    if flight.departure_time >= current_time + (20 if current_city != start_city else 0) and flight.arrival_time <= t2:
                        new_hops = hops + 1
                        new_cost = cost + flight.fare
                        new_path = path + [flight]
                        
                        # Only insert the flight if (fewer hops or cheaper)
                        if new_hops < flight.best_hops or (new_hops == flight.best_hops and new_cost < flight.best_cost):
                            flight.best_hops = new_hops
                            flight.best_cost = new_cost
                            heap.insert((new_hops, new_cost, flight.end_city, flight.arrival_time, new_path))
            
            return best_route if best_route else []

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self,x):
        self.items.append(x)
    
    def dequeue(self):
        if len(self.items) != 0:
            x = self.items.pop(0)
            return x
        return None

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return len(self.items) == 0

class Node:
    def __init__(self) :
        self.destinations = []
        self.best_path = []
        self.visited = False
        self.total_cost = 0