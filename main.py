import heapq

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.traffic_patterns = {} 

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = {}

    def add_edge(self, node1, node2, weight):
        self.edges[node1][node2] = weight
        self.edges[node2][node1] = weight

    def add_traffic_pattern(self, node, hour, multiplier):
        if node not in self.traffic_patterns:
            self.traffic_patterns[node] = {}
        self.traffic_patterns[node][hour] = multiplier

    def get_effective_weight(self, node1, node2, current_time_hour):
        base_weight = self.edges[node1].get(node2, float('inf'))
        
        
        traffic_multiplier = self.traffic_patterns.get(node2, {}).get(current_time_hour, 1.0)
        
        return base_weight * traffic_multiplier

def find_shortest_path_with_traffic(graph, start_node, end_node, start_time_hour):

    
    
    priority_queue = [(0, start_node, [start_node], start_time_hour)]
    

    min_cost = {(start_node, start_time_hour): 0} 

    while priority_queue:
        current_cost, current_node, path, current_time_at_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            return current_cost, path


        if current_cost > min_cost.get((current_node, current_time_at_node), float('inf')):
            continue

        for neighbor, base_weight in graph.edges[current_node].items():

            effective_weight = graph.get_effective_weight(current_node, neighbor, current_time_at_node)
            

            travel_duration_hours = effective_weight 
            next_time_at_neighbor = (current_time_at_node + int(travel_duration_hours)) % 24

            new_cost = current_cost + effective_weight


            if new_cost < min_cost.get((neighbor, next_time_at_neighbor), float('inf')):
                min_cost[(neighbor, next_time_at_neighbor)] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor], next_time_at_neighbor))

    return float('inf'), [] 


if __name__ == "__main__":
    city_graph = Graph()


    nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    for node in nodes:
        city_graph.add_node(node)


    city_graph.add_edge('A', 'B', 2)
    city_graph.add_edge('A', 'C', 4)
    city_graph.add_edge('B', 'D', 3)
    city_graph.add_edge('C', 'D', 1)
    city_graph.add_edge('D', 'E', 2)
    city_graph.add_edge('E', 'F', 1)
    city_graph.add_edge('B', 'E', 5)


    city_graph.add_traffic_pattern('D', 8, 2.5)  
    city_graph.add_traffic_pattern('D', 17, 2.0) 
    city_graph.add_traffic_pattern('E', 9, 1.8) 

    start = 'A'
    end = 'F'
    
    print("--- Escenario 1: Comenzando a las 7 AM (sin tráfico significativo) ---")
    start_hour_1 = 7
    cost1, path1 = find_shortest_path_with_traffic(city_graph, start, end, start_hour_1)
    if cost1 != float('inf'):
        print(f"Ruta más corta de {start} a {end} comenzando a las {start_hour_1} AM: {path1}")
        print(f"Tiempo total de viaje efectivo: {cost1:.2f} horas")
    else:
        print(f"No se encontró ruta de {start} a {end}.")

    print("\n--- Escenario 2: Comenzando a las 8 AM (entrando en la hora pico matutina) ---")
    start_hour_2 = 8
    cost2, path2 = find_shortest_path_with_traffic(city_graph, start, end, start_hour_2)
    if cost2 != float('inf'):
        print(f"Ruta más corta de {start} a {end} comenzando a las {start_hour_2} AM: {path2}")
        print(f"Tiempo total de viaje efectivo: {cost2:.2f} horas")
    else:
        print(f"No se encontró ruta de {start} a {end}.")