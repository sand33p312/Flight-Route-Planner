from flight import Flight
from planner import Planner

def main():
    flights = [Flight(0, 0, 0, 1, 30, 50),      # City 0 to 1
               Flight(1, 0, 0, 3, 80, 200),     # City 0 to 3
               
               Flight(2, 1, 40, 2, 60, 20),     # City 1 to 2
               Flight(3, 1, 50, 2, 100, 120),   # City 1 to 2
               
               Flight(4, 2, 120, 4, 200, 100),  # City 2 to 4
               
               Flight(5, 3, 100, 4, 150, 500),  # City 3 to 4
               Flight(6, 3, 100, 4, 250, 300)   # City 3 to 4
               ]
    
    flight_planner = Planner(flights)
    
    # The three tasks
    route1 = flight_planner.least_flights_ealiest_route(0, 4, 0, 300)
    route2 = flight_planner.cheapest_route(0, 4, 0, 300)
    route3 = flight_planner.least_flights_cheapest_route(0, 4, 0, 300)
    
    # model output
    expected_route1 = [flights[1], flights[5]]                  # 0-3-4, 2 flights, arrives at t=150
    expected_route2 = [flights[0], flights[3], flights[4]]      # 0-1-2-4, 270 fare
    expected_route3 = [flights[1], flights[6]]                  # 0-3-4, 2 flights, 500 fare
    
    # Note that for this given example there is a unique solution, but it may
    # not be true in general
    if route1 == expected_route1:
        print("Task 1 PASSED")
        
    if route2 == expected_route2:
        print("Task 2 PASSED")
        
    if route3 == expected_route3:
        print("Task 3 PASSED")
        

if __name__ == "__main__":
    main()