import json
from types import SimpleNamespace

from DiGraph import Node, Edge, DiGraph
import Algo
# from Ex4.client_python.Algo import Algo
from client import Client


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph
        self.algo = None
        self.pokemon = {}
        # default port
        PORT = 6666
        # server host (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        self.client = Client()
        self.client.start_connection(HOST, PORT)

    def load_json(self):

        graph_json = self.client.get_graph()
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

        self.algo = Algo.Algo(self.g)


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
        pokemons = json.loads(self.client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            self.pokemon[p.pos] = p
        for p in self.pokemon.values():
            print(p)
            w = p.pos.split(',')
            sr = w[0]
            ds = w[1]
            for i in self.algo.edges:
                s = i.split(',')
                src = s[0]
                dst = s[1]
                if self.algo.distance(src, dst, sr, ds, p.type) is not None:
                    ans = self.algo.distance(src, dst, sr, ds, p.type)
            print(ans)



def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    t.get_pokemon()





if __name__ == '__main__':
    main()
