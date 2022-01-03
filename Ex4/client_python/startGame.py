from types import SimpleNamespace

from Ex4.client_python.DiGraph import DiGraph, Edge, Node
import json
from client import Client


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph
        self.pokemon = {}

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
        client.start()

        pokemons = client.get_pokemons()
        pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
        poke[]
        print(self.pokemon)

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.g

    def is_nei(self, id: int):
        list = []
        for i in self.g.graphDict.get(id).outEdge:
            list.append(self.g.graphDict.get(id).outEdge.get(i))
        return list

    def get_pokemon(self):
        PORT = 6666
        # server host (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        client = Client()
        client.start_connection(HOST, PORT)
        poke = client.get_pokemons()
        pokemons = json.loads(poke, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        self.pokemon[pokemons.__dict__.get("pos")] = pokemons
        print(self.pokemon)


def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    for i in t.get_graph().graphDict.values():
        print(i)
        print(t.is_nei(1))

        print("in edge:", i.inEdge)
        print("out edge: ", i.outEdge)





if __name__ == '__main__':
    main()
