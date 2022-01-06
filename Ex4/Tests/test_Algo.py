import json
import unittest
from types import SimpleNamespace

import GraphAlgo
import players
from DiGraph import DiGraph, Node, Edge
from Algo import Algo
from startGame import startGame


class Tests(unittest.TestCase):

##Digraph tests
    def test_add(self):
        g = DiGraph()
        cc = g.add_node(1, ("2", "2", "3"))
        self.assertTrue(cc)
        v = g.graphDict[1]
        self.assertEqual(g.graphDict[1], v)

    def test_remove_node(self):
        g = DiGraph()
        self.assertFalse(g.remove_node(1))
        c = g.add_node(1, ("2", "2", "2"))
        self.assertTrue(g.remove_node(1))
        self.assertIsNone(g.graphDict.get(3))

    def test_add_Edge(self):
        g = DiGraph()
        g.add_node(2, ("3", "3", "0"))
        g.add_node(1, ("3", "3", "0"))
        self.assertTrue(g.add_edge(1, 2, 5.4))

    def test_remove_Edge(self):
        g = DiGraph()
        g.add_node(2, ("3", "3", "0"))
        g.add_node(1, ("3", "3", "0"))
        g.add_edge(1, 2, 5.4)
        self.assertTrue(g.remove_edge(1, 2))
        g.add_edge(1, 2, 5.4)
        del (g.graphDict.get(1).outEdge)[2]
        self.assertFalse(g.remove_edge(1, 2))

    def test_in_edge(self):
        g = DiGraph()
        g.add_node(1, ("3", "3", "0"))
        g.add_node(2, ("3", "3", "0"))
        g.add_node(3, ("3", "3", "0"))
        g.add_edge(1, 2, 77)
        g.add_edge(2, 1, 44)
        g.add_edge(3, 1, 27)
        g.add_edge(3, 2, 27)
        self.assertEqual(g.all_in_edges_of_node(1), {2: 44, 3: 27})
        self.assertEqual(g.all_out_edges_of_node(3), {1: 27, 2: 27})

    def test_getEdgeBySrc(self):
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_node(4)
        g.add_edge(1, 2, 11)
        g.add_edge(1, 3, 12)
        g.add_edge(1, 4, 12)
        g.add_edge(2, 1, 23)
        list = [2, 3, 4]
        self.assertEqual(list, g.getEdgeBySrc(1))

    def test_getweightbysrc(self):
        g = DiGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_node(4)
        g.add_edge(1, 2, 11)
        g.add_edge(1, 3, 12)
        g.add_edge(1, 4, 12)
        g.add_edge(2, 1, 23)
        self.assertEqual(11, g.getWeightOfEdge(1, 2))
        self.assertEqual(23, g.getWeightOfEdge(2, 1))

    ##Algo Tests
    def test_shortest_path(self):
        g = DiGraph()
        s = Algo(g)
        s.g.add_node(0)
        s.g.add_node(1)
        s.g.add_node(2)
        s.g.add_edge(0, 1, 1)
        s.g.add_edge(1, 2, 4)
        self.assertEqual([5.0, [0, 1, 2]], s.shortest_path(0, 1, 2))
        # self.assertEqual(s.algo.shortest_path(0, 1,2), (5, [0, 1, 2]))

    def test_distance(self):
        g = DiGraph()
        graphAlgo = Algo(g)
        graphAlgo.load_json_file(r"C:\Users\avi44\PycharmProjects\Ex4-oop\Ex4\data\check_graph.json")
        test_agent = {'Agent':
                    {'id': 0,
                     'value': 0.0,
                     'src': 9,
                     'dest': 8,
                     'speed': 1.0,
                     'pos': '35.206561379997034,32.10572672919794,0.0'}}

        a = players.agent(test_agent)
        print(graphAlgo.min_price(a,1,2))
        self.assertEqual(2,graphAlgo.min_price(a,1,2))

    def test_time_to_take(self):
        g = DiGraph()
        graphAlgo = Algo(g)
        w = 10
        s = 5
        self.assertEqual(2,graphAlgo.time_to_take(s,w))

    def test_dist(self):
        g = DiGraph()
        graphAlgo = Algo(g)
        graphAlgo.load_json_file(r"C:\Users\avi44\PycharmProjects\Ex4-oop\Ex4\data\check_graph.json")
        pok_pos_x=35.1875942163034
        pok_pos_y=32.103782258823
        type1 = 1
        self.assertEqual(('14', '15'),graphAlgo.distance("14","15",pok_pos_x,pok_pos_y,type1))




