import unittest
from typing import Iterable
from truck_simulator.core.graph import Node, Edge, make_edge, Path, make_path_from_edge_list, step, walk
from truck_simulator.core.graph import Graph, make_graph, get_edge, get_neighborhood
class TestGraph(unittest.TestCase):

    def test_make_edge(self):
        # Test creating an edge between two nodes
        node1: Node = "AP"
        node2: Node = "BA"
        edge: Edge = make_edge(node1, node2)
        self.assertEqual(edge.nodes, (node1, node2))
        self.assertEqual(edge.weight, 1)

    def test_make_path_from_edge_list(self):
        node1: Node = "AM"
        node2: Node = "BA"
        node3: Node = "CE"
        node4: Node = "DF"
        edge_list: Iterable[Edge] = map(make_edge, *zip(*[(node1, node2), (node2, node3), (node3, node4)]))
        path: Path = make_path_from_edge_list(node1, edge_list)
        self.assertEqual(path.start, node1)
        self.assertEqual(path.data, {node1: node2, node2: node3, node3: node4})

    def test_step(self):
        node1: Node = "AP"
        node2: Node = "BA"
        node3: Node = "CE"
        node4: Node = "DF"
        edge_list: Iterable[Edge] = map(make_edge, *zip(*[(node1, node2), (node2, node3), (node3, node4)]))
        path: Path = make_path_from_edge_list(node1, edge_list)
        self.assertEqual(step(path, node1), node2)
        self.assertEqual(step(path, node2), node3)
        self.assertEqual(step(path, node3), node4)

    def test_walk(self):
        node1: Node = "AP"
        node2: Node = "BA"
        node3: Node = "CE"
        node4: Node = "DF"
        edge_list: Iterable[Edge] = map(make_edge, *zip(*[(node1, node2), (node2, node3), (node3, node4)]))
        path: Path = make_path_from_edge_list(node1, edge_list)
        self.assertEqual(list(walk(path, node1)), [node2, node3, node4])
        self.assertEqual(list(walk(path, node2)), [node3, node4])
        self.assertEqual(list(walk(path, node3)), [node4])

    def test_make_graph(self):
        # Test creating a graph with one node and no edges
        node1: Node = "AP"
        graph: Graph = make_graph({node1}, set())
        self.assertEqual(graph.nodes, {node1})
        self.assertEqual(graph.edges, set())
        self.assertEqual(graph.adjacency_list, {node1: set()})

        # Test creating a graph with multiple nodes and edges
        node2: Node = "BA"
        node3: Node = "CE"
        edge1: Edge = make_edge(node1, node2)
        edge2: Edge = make_edge(node2, node3)
        graph: Graph = make_graph({node1, node2, node3}, {edge1, edge2})
        self.assertEqual(graph.nodes, {node1, node2, node3})
        self.assertEqual(graph.edges, {edge1, edge2})
        self.assertEqual(graph.adjacency_list, {node1: {(node2, 1)}, node2: {(node1, 1), (node3, 1)}, node3: {(node2, 1)}})

    def test_get_edge(self):
        node1: Node = "AC"
        node2: Node = "BA"
        node3: Node = "CE"
        edge1: Edge = make_edge(node1, node2, 5)
        edge2: Edge = make_edge(node2, node3, 10)
        graph = make_graph({node1, node2, node3}, {edge1, edge2})
        self.assertEqual(get_edge(node1, node2, graph), edge1)
        self.assertEqual(get_edge(node2, node3, graph), edge2)
        self.assertEqual(get_edge(node1, node3, graph), None)

    def test_get_neighborhood(self):
        # Test getting the neighborhood of a node with no neighbors
        node1: Node = "AP"
        graph: Graph = make_graph({node1}, set())
        self.assertEqual(get_neighborhood(node1, graph), set())

        # Test getting the neighborhood of a node with neighbors
        node2: Node = "BA"
        node3: Node = "CE"
        edge1: Edge = make_edge(node1, node2)
        edge2: Edge = make_edge(node2, node3)
        graph: Graph = make_graph({node1, node2, node3}, {edge1, edge2})
        self.assertEqual(get_neighborhood(node1, graph), {(node2, 1)})
        self.assertEqual(get_neighborhood(node2, graph), {(node1, 1), (node3, 1)})
        self.assertEqual(get_neighborhood(node3, graph), {(node2, 1)})

    # TODO test get_edge
    # TODO test make_path

if __name__ == "__main__":
    unittest.main()