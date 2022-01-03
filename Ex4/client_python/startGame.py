from types import SimpleNamespace
from client import Client
import json


class DiGraph:

    def __init__(self):
        """"we save all the nodes and the updating in the graph"""
        self.graphDict = {}  # {key :node_id, value: node_data}
        self.mc = 0

    def v_size(self) -> int:

        """ return the number of vertex in the graph"""
        return self.Nodes.__len__()

    def e_size(self) -> int:

        """ return the number of Edge in the graph"""
        return self.Edges.__len__()

    def get_all_v(self) -> dict:
        """"return all the graph vertical in dictionary <key, Node>"""
        return self.graphDict

    def all_in_edges_of_node(self, id1: int) -> dict:

        """":param the id of the node
        :return all the edge that get into this vertical <key of src, wight>"""
        return self.graphDict.get(id1).inEdge
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """

    def all_out_edges_of_node(self, id1: int) -> dict:
        """":param the id of the node
           :return all the edge that get from the node to other <key of src, wight>"""
        return self.graphDict.get(id1).outEdge

    def get_mc(self) -> int:
        """represent the number of changes that does on the graph """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.graphDict.get(id1) is None or self.graphDict.get(id2) is None:
            return False
        if self.graphDict.get(id1).outEdge.get(id2) is None and self.graphDict.get(id2).inEdge.get(id1) is None:
            self.graphDict.get(id1).outEdge[id2] = weight
            self.graphDict.get(id2).inEdge[id1] = weight
            self.mc += 1
            return True
        return False
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: 
         will do nothing
        """

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        self.mc = self.mc + 1
        if self.graphDict.get(node_id) is not None:
            return False
        """ checking why we need to insert empty pos"""
        if pos is None:
            list = {}
            list["id"] = node_id
            list["pos"] = ""
            node = Node(list)
            self.graphDict[node_id] = node
            return True
        list = {}

        if type(pos) is str:
            list["pos"] = pos
            list["id"] = node_id
            s = SimpleNamespace(**list)
            node = Node(s)
            self.graphDict[node_id] = node
            return True
        s = str(pos[0])
        for st in pos[1:]:
            s += "," + str(st)
        list["id"] = node_id
        list["pos"] = s
        node = Node(list)
        self.graphDict[node_id] = node
        return True

    def remove_node(self, node_id: int) -> bool:
        if self.graphDict.__contains__(node_id):
            self.graphDict.pop(node_id)
            return True
        return False
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """

    #
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        self.mc += 1
        if self.graphDict.get(node_id1).outEdge.get(node_id2) is None or self.graphDict.get(node_id2).inEdge.get(
                node_id1) is None:
            return False
        del (self.graphDict.get(node_id1).outEdge)[node_id2]
        del (self.graphDict.get(node_id2).inEdge)[node_id1]
        return True

        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """

    def getEdgeBySrc(self, v: int) -> list:
        """this function get node id and return a list of all of its neighbors"""
        list = []
        for i in self.graphDict.get(v).outEdge:
            list.append(i)
        return list

    def getWeightOfEdge(self, src: int, dest: int) -> float:
        """get: the src and dst of edge
        return: the wight"""
        return self.graphDict.get(src).outEdge[dest]

    """""convert string of geoLocation to float parameters"""

    def posGetX(self, pos: str):
        s = pos.split(',')
        return s[0]

    def posGetY(self, pos: str):
        s = pos.split(',')
        return s[1]


class Edge:
    def __init__(self, list:SimpleNamespace):
        self.src = list.__dict__.get("src")
        self.w = list.__dict__.get("w")
        self.dest = list.__dict__.get("dest")

    def __repr__(self):
        return f"src: {self.src} dst: {self.dest} wight: {self.w}"

    def __str__(self):
        return f"src: {self.src} dst: {self.dest} wight: {self.w}"


class Node:
    def __init__(self, list:SimpleNamespace):
        self.id = list.__dict__.get("id")
        self.pos = list.__dict__.get("pos")
        self.inEdge = {}  # this is dic of edge into our node <"other node.id",w>
        self.outEdge = {}  # this is dic of edge from our node <"other node.id",w>

    def __iter__(self):
        return self.inEdge

    def __repr__(self):
        return f"(id: {self.id} node pos: {self.pos})"

    def __str__(self):
        return f"(node id: {self.id} node pos: {self.pos})"


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph

    def load_json(self):
        # default port
        PORT = 6666
        # server host (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        client = Client()
        client.start_connection(HOST, PORT)
        graph_json = client.get_graph()
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

        for n in Nodes:
            s = n.pos.split(',')
            x = s[0]
            y = s[1]


    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.g

    def is_nei(self,id:int):
        list = []
        for i in self.g.graphDict.get(id).outEdge:
            list.append(self.g.graphDict.get(id).outEdge.get(i))
        return list




def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    for i in t.get_graph().graphDict.values():
        print(i)
        print(t.is_nei(1))

        print("in edge:", i.inEdge)
        print("out edge: ", i.outEdge)

    # # default port
    # PORT = 6666
    # # server host (default localhost 127.0.0.1)
    # HOST = '127.0.0.1'
    # client = Client()
    # client.start_connection(HOST, PORT)
    # graph_json = client.get_graph()
    # graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
    # Nodes = []
    # Edges = []
    # for n in graph.Nodes:
    #     Nodes.append(Node(n))
    # for e in graph.Edges:
    #     Edges.append(Edge(e))
    #
    #
    # for n in Nodes:
    #     s = n.pos.split(',')
    #     x = s[0]
    #     y = s[1]
    #     print(x)


if __name__ == '__main__':
    main()
