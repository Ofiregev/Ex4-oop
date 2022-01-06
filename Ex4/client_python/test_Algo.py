import json
import unittest
from unittest import TestCase
from DiGraph import DiGraph, Node
from Algo import Algo


class Tests(unittest.TestCase):
    def test_shortest_path(self):
        g = DiGraph()
        graph_json = Algo.client.get_graph()
        graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        Nodes = []
        Edges = []
        for n in graph.Nodes:
            Nodes.append(Node(n))
        for e in graph.Edges:
            Edges.append(Edge(e))
        for i in Nodes:
            self.g.add_node(i.id, i.pos)
        for i in Edges:
            self.g.add_edge(i.src, i.dest, i.w)
        d = Algo(g)
        self.assertEqual([4, [0, 2, 1]], d.shortest_path(0, 1))
        self.assertEqual([float('inf'), []], d.shortest_path(1, 4))
