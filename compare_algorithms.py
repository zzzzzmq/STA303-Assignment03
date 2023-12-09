from typing import List
from plot_underground_path import plot_path
from build_data import Station, build_data
import math
import argparse
from heapq import heappop, heappush
import time


def dijkstra_get_path(start_station_name: str, end_station_name: str, map: dict[str, Station]) -> List[str]:
    """
    runs Dijkstra's algorithm on the map, find the shortest path between a and b
    Args:
        start_station_name(str): The name of the starting station
        end_station_name(str): str The name of the ending station
        map(dict[str, Station]): Mapping between station names and station objects of the name
    Returns:
        List[str]: A path composed of a series of station names
    """
    def distance(station1, station2):
        x1, y1 = station1.position
        x2, y2 = station2.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    start_station = map[start_station_name]
    end_station = map[end_station_name]
    
    # Given a Station object, you can obtain the name and latitude and longitude of that Station by the following code
#    print(f'The longitude and latitude of the {start_station.name} is {start_station.position}')
#    print(f'The longitude and latitude of the {end_station.name} is {end_station.position}')
    
    # Priority queue for the open set
    open_set = [(0, start_station, [])]
    # Dictionary to keep track of the current best known cost to reach each station
    best_known_costs = {start_station: 0}

    while open_set:
        current_cost, current_station, current_path = heappop(open_set)

        if current_station == end_station:
            # Return the path when reaching the destination
            return current_path + [current_station.name]

        for neighbor in current_station.links:
            tentative_cost = current_cost + distance(current_station, neighbor)

            if neighbor not in best_known_costs or tentative_cost < best_known_costs[neighbor]:
                best_known_costs[neighbor] = tentative_cost
                heappush(open_set, (tentative_cost, neighbor, current_path + [current_station.name]))

    return []

def a_star_get_path(start_station_name: str, end_station_name: str, map: dict[str, Station]) -> List[Station]:
    """
    Runs A* algorithm on the map, find the shortest path between a and b
    Args:
        start_station_name(str): The name of the starting station
        end_station_name(str): The name of the ending station
        map(dict[str, Station]): Mapping between station names and station objects of the name
    Returns:
        List[Station]: A path composed of a series of Station objects
    """
    def distance(station1, station2):
        x1, y1 = station1.position
        x2, y2 = station2.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Heuristic function for A*
    def heuristic(node1, node2):
        return distance(node1, node2)

    # You can obtain the Station objects of the starting and ending station through the following code
    start_station = map[start_station_name]
    end_station = map[end_station_name]
    # Given a Station object, you can obtain the name and latitude and longitude of that Station by the following code
    print(f'The longitude and latitude of the {start_station.name} is {start_station.position}')
    print(f'The longitude and latitude of the {end_station.name} is {end_station.position}')
    
    # Priority queue for the open set
    open_set = [(0, start_station, [])]  # Updated: Include an empty list for the current path
    # Set to keep track of visited stations
    visited = set()
    
    while open_set:
        current_cost, current_station, current_path = heappop(open_set)

        if current_station == end_station:
            # Return the path when reaching the destination
            return current_path + [current_station.name]

        if current_station in visited:
            continue

        visited.add(current_station)

        for neighbor in current_station.links:
            if neighbor in visited:
                continue

            tentative_cost = current_cost + distance(current_station, neighbor)
            heuristic_cost = tentative_cost + distance(neighbor, end_station)
            heappush(open_set, (heuristic_cost, neighbor, current_path + [current_station.name]))
            
    return []

def bellman_ford_get_path(start_station_name: str, end_station_name: str, map: dict[str, Station]) -> List[Station]:
    """
    Runs Bellman-Ford algorithm on the map, find the shortest path between a and b
    Args:
        start_station_name(str): The name of the starting station
        end_station_name(str): The name of the ending station
        map(dict[str, Station]): Mapping between station names and station objects of the name
    Returns:
        List[Station]: A path composed of a series of Station objects
    """
    def distance(station1, station2):
        x1, y1 = station1.position
        x2, y2 = station2.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # You can obtain the Station objects of the starting and ending station through the following code
    start_station = map[start_station_name]
    end_station = map[end_station_name]
    # Given a Station object, you can obtain the name and latitude and longitude of that Station by the following code
    print(f'The longitude and latitude of the {start_station.name} is {start_station.position}')
    print(f'The longitude and latitude of the {end_station.name} is {end_station.position}')
    
    # Initialize distances and predecessor lists
    distances = {station_name: float('inf') for station_name in map}
    predecessors = {station_name: None for station_name in map}
    distances[start_station_name] = 0
    
    # Relax edges repeatedly
    for _ in range(len(map) - 1):
        for current_station_name, current_station in map.items():
            for neighbor_name in current_station.links:
                neighbor_station = map[neighbor_name]
                edge_weight = distance(current_station, neighbor_station)
                if distances[current_station_name] + edge_weight < distances[neighbor_name]:
                    distances[neighbor_name] = distances[current_station_name] + edge_weight
                    predecessors[neighbor_name] = current_station_name
    
    # Check for negative cycles
    for current_station_name, current_station in map.items():
        for neighbor_name in current_station.links:
            neighbor_station = map[neighbor_name]
            edge_weight = distance(current_station, neighbor_station)
            if distances[current_station_name] + edge_weight < distances[neighbor_name]:
                # Negative cycle detected, handle as needed
                return []

    # Reconstruct the path
    path = []
    current = end_station_name
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]

    return path


def calculate_path_length(path, map):
    # Assuming the path is a list of station names
    length = 0
    for i in range(len(path)-1):
        length += distance(map[path[i]], map[path[i+1]])
    return length

def distance(station1, station2):
    x1, y1 = station1.position
    x2, y2 = station2.position
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


if __name__ == '__main__':
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('start_station_name', type=str, help='start_station_name')
    parser.add_argument('end_station_name', type=str, help='end_station_name')
    args = parser.parse_args()
    start_station_name = args.start_station_name
    end_station_name = args.end_station_name

    # The relevant descriptions of stations and underground_lines can be found in the build_data.py
    stations_map, underground_lines = build_data()

    # Run Dijkstra's algorithm
    start_time_dijkstra = time.time()
    path_dijkstra = dijkstra_get_path(start_station_name, end_station_name, stations_map)
    elapsed_time_dijkstra = time.time() - start_time_dijkstra
    path_length_dijkstra = calculate_path_length(path_dijkstra, stations_map)

    # Run A* algorithm
    start_time_a_star = time.time()
    path_a_star = a_star_get_path(start_station_name, end_station_name, stations_map)
    elapsed_time_a_star = time.time() - start_time_a_star
    path_length_a_star = calculate_path_length(path_a_star, stations_map)

    # Run bellman_ford algorithm
    start_time_bellman_ford = time.time()
    path_bellman_ford = bellman_ford_get_path(start_station_name, end_station_name, stations_map)
    elapsed_time_bellman_ford = time.time() - start_time_bellman_ford
    path_length_bellman_ford = calculate_path_length(path_bellman_ford, stations_map)
    
    # Compare results
    print(f"Dijkstra's - Elapsed Time: {elapsed_time_dijkstra}, Path Length: {path_length_dijkstra}")
    print(f"A* - Elapsed Time: {elapsed_time_a_star}, Path Length: {path_length_a_star}")
    print(f"Bellman_ford - Elapsed Time: {elapsed_time_bellman_ford}, Path Length: {path_length_bellman_ford}")
    
    # Compare path lengths
    if path_length_dijkstra < path_length_a_star and path_length_dijkstra < path_length_bellman_ford:
        print("Dijkstra's found the shortest path.")
    elif path_length_a_star < path_length_dijkstra and path_length_a_star < path_length_bellman_ford:
        print("A* found the shortest path.")
    elif path_length_bellman_ford < path_length_dijkstra and path_length_bellman_ford < path_length_a_star:
        print("Bellman-Ford found the shortest path.")
    # Compare path lengths to find the longest path
    elif path_length_dijkstra > path_length_a_star and path_length_dijkstra > path_length_bellman_ford:
        print("Dijkstra's found the longest path.")
    elif path_length_a_star > path_length_dijkstra and path_length_a_star > path_length_bellman_ford:
         print("A* found the longest path.")
    elif path_length_bellman_ford > path_length_dijkstra and path_length_bellman_ford > path_length_a_star:
         print("Bellman-Ford found the longest path.")
    else:
        print("All algorithms found paths with the same length.")
     
