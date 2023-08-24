from dataclasses import dataclass
from typing import List, Tuple, Dict, TypeAlias, Optional, Generator
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
    weight: int

def make_node(location: Location, coordintes: GeoLocation, weight: Optional[int] = None) -> Node:
    """
    Create a node on the graph.

    Args:
        location (Location): the name of the location on the map.
        coordintes (GeoLocation): the coordinates of the location on the map.

    Returns:
        Node: the node on the graph.
    """
    return Node(location, coordintes, weight or 1)

Edge: TypeAlias = Tuple[Node, Node]

def make_edge(node1: Node, node2: Node) -> Edge:
    """
    Create an edge between two nodes.

    Args:
        node1 (Node): the first node.
        node2 (Node): the second node.

    Returns:
        Edge: the edge between the two nodes.
    """
    return (node1, node2)


@dataclass
class Path:
    """
    A path between two nodes.

    Attributes:
        start (Node): the starting node.
        data (Dict[Node, Node]): the path between two nodes.
    """
    start: Node
    data: Dict[Location, Node]

    
def step(path, curr: Node) -> Node:
    """
    Get the next node on the path.

    Args:
        curr (Node): the current node.

    Returns:
        Node: the next node on the path.
    """
    return path.data[curr.location]

def walk(path, curr: Optional[Node] = None) -> Generator[Node, None, None]:
    """
    Get the path as a list of nodes.

    Returns:
        List[Node]: the path as a list of nodes.
    """
    curr: Node = curr or path.start

    # checks only dictionary keys
    while curr.location in path.data:
        yield step(path, curr)
        curr = step(path, curr)

def make_path_from_edge_list(start: Node, edge_list: List[Edge]) -> Path:
    """
    Create a path from a list of edges.

    Args:
        start (Node): the starting node.
        edge_list (List[Edge]): the list of edges.

    Returns:
        Path: the path from the starting node.
    """
    path: Dict[Node, Node] = {}
    for edge in edge_list:
        path[edge[0].location] = edge[1]
    return Path(start, path)

    

@dataclass
class Graph:
    """
    A graph representation of a map.

    Attributes:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.
        adjacency_list (Dict[Node, List[Node]]): the adjacency list representation of the graph.
    """
    nodes: List[Node]
    edges: List[Edge]
    adjacency_list: Dict[Location, List[Node]]

def make_graph(nodes: List[Node], edges: List[Edge]) -> Graph:
    """
    Create a graph representation of a map.

    Args:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.

    Returns:
        Graph: the graph representation of a map.
    """
    adjacency_list: Dict[Location, List[Node]] = {}
    for node in nodes:
        adjacency_list[node.location] = []
    for edge in edges:
        adjacency_list[edge[0].location].append(edge[1])
        adjacency_list[edge[1].location].append(edge[0])

    return Graph(nodes, edges, adjacency_list)

def get_neighborhood(node: Node, graph: Graph) -> List[Node]:
    """
    Get the neighboorhood of a node.

    Args:
        node (Node): the node to get the neighboorhood.
        graph (Graph): the graph to get the neighboorhood.

    Returns:
        List[Node]: the neighboorhood of the node.
    """
    return graph.adjacency_list[node.location]

