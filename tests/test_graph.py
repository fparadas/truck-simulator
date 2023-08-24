import unittest
from truck_simulator.core.types import GeoLocation
from truck_simulator.core.graph import make_node, make_edge, make_path_from_edge_list, step, walk, make_graph, get_neighborhood

class TestGraph(unittest.TestCase):
    def test_make_node(self):
        # Test creating a node with default weight
        node1 = make_node("AP", GeoLocation(0, 0))
        self.assertEqual(node1.location, "AP")
        self.assertEqual(node1.coordintes.latitude, 0)
        self.assertEqual(node1.coordintes.longitude, 0)

    def test_make_edge(self):
        # Test creating an edge between two nodes
        node1 = make_node("AP", GeoLocation(0, 0))
        node2 = make_node("BA", GeoLocation(1, 1))
        edge = make_edge(node1, node2)
        self.assertEqual(edge.nodes, (node1, node2))
        self.assertEqual(edge.weight, 1)

    def test_make_path_from_edge_list(self):
        node1 = make_node("AM", GeoLocation(0, 0))
        node2 = make_node("BA", GeoLocation(0, 0))
        node3 = make_node("CE", GeoLocation(0, 0))
        node4 = make_node("DF", GeoLocation(0, 0))
        edge_list = [make_edge(node1, node2), make_edge(node2, node3), make_edge(node3, node4)]
        path = make_path_from_edge_list(node1, edge_list)
        self.assertEqual(path.start, node1)
        self.assertEqual(path.data, {node1.location: node2, node2.location: node3, node3.location: node4})

    def test_step(self):
        node1 = make_node("AP", GeoLocation(0, 0))
        node2 = make_node("BA", GeoLocation(0, 0))
        node3 = make_node("CE", GeoLocation(0, 0))
        node4 = make_node("DF", GeoLocation(0, 0))
        edge_list = [make_edge(node1, node2), make_edge(node2, node3), make_edge(node3, node4)]
        path = make_path_from_edge_list(node1, list(edge_list))
        self.assertEqual(step(path, node1), node2)
        self.assertEqual(step(path, node2), node3)
        self.assertEqual(step(path, node3), node4)

    def test_walk(self):
        node1 = make_node("AP", GeoLocation(0, 0))
        node2 = make_node("BA", GeoLocation(0, 0))
        node3 = make_node("CE", GeoLocation(0, 0))
        node4 = make_node("DF", GeoLocation(0, 0))
        edge_list = [make_edge(node1, node2), make_edge(node2, node3), make_edge(node3, node4)]
        path = make_path_from_edge_list(node1, list(edge_list))
        self.assertEqual(list(walk(path, node1)), [node2, node3, node4])
        self.assertEqual(list(walk(path, node2)), [node3, node4])
        self.assertEqual(list(walk(path, node3)), [node4])

    def test_make_graph(self):
        # Test creating a graph with one node and no edges
        node1 = make_node("AP", (0, 0))
        graph = make_graph({node1}, set())
        self.assertEqual(graph.nodes, {node1})
        self.assertEqual(graph.edges, set())
        self.assertEqual(graph.adjacency_list, {node1.location: set()})

        # Test creating a graph with multiple nodes and edges
        node2 = make_node("BA", (1, 1))
        node3 = make_node("CE", (2, 2))
        edge1 = make_edge(node1, node2)
        edge2 = make_edge(node2, node3)
        graph = make_graph({node1, node2, node3}, {edge1, edge2})
        self.assertEqual(graph.nodes, {node1, node2, node3})
        self.assertEqual(graph.edges, {edge1, edge2})
        self.assertEqual(graph.adjacency_list, {node1.location: {(node2, 1)}, node2.location: {(node1, 1), (node3, 1)}, node3.location: {(node2, 1)}})

    def test_get_neighborhood(self):
        # Test getting the neighborhood of a node with no neighbors
        node1 = make_node("AP", (0, 0))
        graph = make_graph({node1}, set())
        self.assertEqual(get_neighborhood(node1, graph), set())

        # Test getting the neighborhood of a node with neighbors
        node2 = make_node("BA", (1, 1))
        node3 = make_node("CE", (2, 2))
        edge1 = make_edge(node1, node2)
        edge2 = make_edge(node2, node3)
        graph = make_graph({node1, node2, node3}, {edge1, edge2})
        self.assertEqual(get_neighborhood(node1, graph), {(node2, 1)})
        self.assertEqual(get_neighborhood(node2, graph), {(node1, 1), (node3, 1)})
        self.assertEqual(get_neighborhood(node3, graph), {(node2, 1)})

    # TODO test get_edge
    # TODO test make_path

if __name__ == "__main__":
    unittest.main()