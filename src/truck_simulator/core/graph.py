from dataclasses import dataclass
from typing import List, Set, Tuple, Dict, TypeAlias, Optional
from core.types import Location, GeoLocation

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

def make_node(location: Location, coordintes: GeoLocation, weight: Optional[int]) -> Node:
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

Path: TypeAlias = Dict[Node, Node]

def make_path(start: Node, end: Node) -> Path:
    """
    Create a path between two nodes.

    Args:
        start (Node): the start node.
        end (Node): the end node.

    Returns:
        Path: the path between the two nodes.
    """
    return {start: end}

def walk_step(start: Node, path: Path) -> Node:
    """
    Walk one step on the path.

    Args:
        start (Node): the start node.
        path (Path): the path to walk.

    Returns:
        Node: the next node on the path.
    """
    return path[start]

@dataclass
class Graph:
    """
    A graph representation of a map.

    Attributes:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.
        adjacency_list (Dict[Node, Set[Node]]): the adjacency list representation of the graph.
    """
    nodes: Set[Node]
    edges: Set[Edge]
    adjacency_list: Dict[Node, Set[Node]]

def make_graph(nodes: Set[Node], edges: Set[Edge]) -> Graph:
    """
    Create a graph representation of a map.

    Args:
        nodes (List[Node]): the nodes on the map.
        edges (List[Edge]): the edges between nodes on the map.

    Returns:
        Graph: the graph representation of a map.
    """
    adjacency_list: Dict[Node, Set[Node]] = {}
    for node in nodes:
        adjacency_list[node] = set()
    for edge in edges:
        adjacency_list[edge[0]].add(edge[1])
        adjacency_list[edge[1]].add(edge[0])

    return Graph(nodes, edges, adjacency_list)

def get_neighboorhood(node: Node, graph: Graph) -> Set[Node]:
    """
    Get the neighboorhood of a node.

    Args:
        node (Node): the node to get the neighboorhood.
        graph (Graph): the graph to get the neighboorhood.

    Returns:
        Set[Node]: the neighboorhood of the node.
    """
    return graph.adjacency_list[node]

