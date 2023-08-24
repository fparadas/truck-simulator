import heapq
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Generator, Tuple, TypeAlias, Collection
from truck_simulator.core.types import Location, GeoLocation

"""
A map will be a graph of nodes, where each node contains a location on the map.
"""

@dataclass
class Node:
    """
    A node on the graph.

    Attributes:
        location (Location): the name of the location on the map.
        coordintes (GeoLocation): the coordinates of the location on the map.
    """
    location: Location
    coordintes: GeoLocation

    def __hash__(self) -> Location:
        return hash(self.location)

    def __eq__(self, __value) -> bool:
        return self.location == __value
    
def make_node(location: Location, coordintes: GeoLocation) -> Node:
    """
    Create a node on the graph.

    Args:
        location (Location): the name of the location on the map.
        coordintes (GeoLocation): the coordinates of the location on the map.

    Returns:
        Node: the node on the graph.
    """
    return Node(location, coordintes)

Weight: TypeAlias = int

@dataclass
class Edge:
    """
    An edge between two nodes.

    Attributes:
        nodes (Tuple[Node, Node]): the edge.
        weight (Weight): the weight of the edge.
    """
    nodes: Tuple[Node, Node]
    weight: Weight


    def __hash__(self) -> Location:
        return hash((self.nodes[0], self.nodes[1]))

    def __eq__(self, __value) -> bool:
        return self.nodes == __value.nodes or self.nodes == (__value.nodes[1], __value.nodes[0])

def make_edge(node1: Node, node2: Node, weight: Optional[Weight] = None) -> Edge:
    """
    Create an edge between two nodes.

    Args:
        node1 (Node): the first node.
        node2 (Node): the second node.

    Returns:
        Edge: the edge between the two nodes.
    """
    return Edge((node1, node2), weight or 1)


@dataclass
class Path:
    """
    A path between two nodes.

    Attributes:
        start (Node): the starting node.
        data (Dict[Node, Node]): the path between two nodes.
    """
    start: Node
    data: Dict[Node, Node]

    
def step(path, curr: Node) -> Node:
    """
    Get the next node on the path.

    Args:
        curr (Node): the current node.

    Returns:
        Node: the next node on the path.
    """
    return path.data[curr]

def make_path_from_edge_list(start: Node, edge_list: Collection[Edge]) -> Path:
    """
    Create a path from a list of edges.

    Args:
        start (Node): the starting node.
        edge_list (List[Edge]): the list of edges.

    Returns:
        Path: the path from the starting node.
    """
    path: Dict[Node, Node] = {}
    for edge in set(edge_list):
        path[edge.nodes[0]] = edge.nodes[1]
    return Path(start, path)

def walk(path: Path, curr: Optional[Node] = None) -> Generator[Node, None, None]:
    """
    Get the path as a list of nodes.

    Returns:
        List[Node]: the path as a list of nodes.
    """
    curr: Node = curr or path.start

    # checks only dictionary keys
    while curr in path.data:
        yield step(path, curr)
        curr = step(path, curr)

    

@dataclass
class Graph:
    """
    A graph representation of a map.

    Attributes:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.
        adjacency_list (Dict[Node, List[Node]]): the adjacency list representation of the graph.
    """
    nodes: Set[Node]
    edges: Set[Edge]
    adjacency_list: Dict[Node, Set[Tuple[Node, Weight]]]

def make_graph(nodes: Set[Node], edges: Set[Edge]) -> Graph:
    """
    Create a graph representation of a map.

    Args:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.

    Returns:
        Graph: the graph representation of a map.
    """
    adjacency_list: Dict[Node, List[Node]] = {}
    for node in nodes:
        adjacency_list[node] = set()
    for edge in edges:
        adjacency_list[edge.nodes[0]].add((edge.nodes[1], edge.weight))
        adjacency_list[edge.nodes[1]].add((edge.nodes[0], edge.weight))

    return Graph(nodes, edges, adjacency_list)

def get_edge(node1: Node, node2: Node, graph: Graph) -> Optional[Edge]:
    """
    Get the edge between two nodes.

    Args:
        node1 (Node): the first node.
        node2 (Node): the second node.
        graph (Graph): the graph to get the edge.

    Returns:
        Optional[Edge]: the edge between the two nodes.
    """
    for edge in graph.edges:
        if edge.nodes == (node1, node2) or edge.nodes == (node2, node1):
            return edge
    return None

def get_neighborhood(node: Node, graph: Graph) -> Set[Tuple[Node, Weight]]:
    """
    Get the neighboorhood of a node.

    Args:
        node (Node): the node to get the neighboorhood.
        graph (Graph): the graph to get the neighboorhood.

    Returns:
        List[Node]: the neighboorhood of the node.
    """
    return graph.adjacency_list[node]

def make_path(start: Node, destiny: Node, graph: Graph) -> Path:
    """
    Create a path between two nodes. Implements dijkstra's algorithm.

    Args:
        start (Node): the starting node.
        destiny (Node): the destiny node.
        graph (Graph): the graph to get the neighboorhood.

    Returns:
        Path: the path between the two nodes.
    """

    # Initialize the distance to all nodes as infinity, except for the starting node which is 0
    distances = {node.location: float('inf') for node in graph.nodes}
    distances[start.location] = 0
    
    # Initialize the previous node for each node as None
    previous_nodes = {node.location: None for node in graph.nodes}
    
    # Create a priority queue to store the nodes to visit
    nodes_to_visit = [(0, start)]
    
    while nodes_to_visit:
        # Get the node with the smallest distance from the start
        current_distance, current_node = heapq.heappop(nodes_to_visit)
        
        # If we have reached the destination node, we can stop
        if current_node == destiny:
            break
        
        # Visit all the neighbors of the current node
        for neighbor, weight in get_neighborhood(current_node, graph):
            # Calculate the distance to the neighbor through the current node
            distance = current_distance + weight
            
            # If the new distance is smaller than the previous distance to the neighbor, update it
            if distance < distances[neighbor.location]:
                distances[neighbor.location] = distance
                previous_nodes[neighbor.location] = current_node
                
                # Add the neighbor to the priority queue to visit later
                heapq.heappush(nodes_to_visit, (distance, neighbor))
    
    # If we couldn't reach the destination node, return None
    if distances[destiny] == float('inf'):
        return None
    
    # Build the path by following the previous nodes from the destination to the start
    path = []
    current_node = destiny
    while current_node is not None:
        previous = previous_nodes[current_node.location]
        path.append(get_edge(current_node, previous, graph))
        current_node = previous_nodes[current_node.location]
    
    # Return the path as a Path object
    return make_path_from_edge_list(start, path)