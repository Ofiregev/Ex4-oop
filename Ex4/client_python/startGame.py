import json
import time
from types import SimpleNamespace

import Algo
from DiGraph import Node, Edge, DiGraph
from client import Client


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph
        self.algo = None
        self.pokemon = {}
        self.agents ={}
        self.station ={}
        # default port
        PORT = 6666
        # server host (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.client.add_agent("{\"id\":9}")
        self.client.add_agent("{\"id\":1}")
        self.client.add_agent("{\"id\":2}")
        self.client.add_agent("{\"id\":3}")

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
            w = p.pos.split(',')
            sr = w[0]
            ds = w[1]
            for i in self.algo.edges:
                s = i.split(',')
                src = s[0]
                dst = s[1]
                if self.algo.distance(src, dst, sr, ds, p.type) is not None:
                    ans = self.algo.distance(src, dst, sr, ds, int(p.type))
                    self.station[0] = (self.algo.shortest_path(int(self.agents.get(0).src), int(ans[0]), int(ans[1])))
                    self.station.get(0).pop(0)

    def main_loop(self):
        self.client.start()
        while self.client.is_running() == 'true':
            self.get_agents()
            self.get_pokemon()
            self.next_station()
            time.sleep(0.1)

    def get_agents(self):
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            self.agents[a.id] = a
            self.station[a.id] = []

    def next_station(self):
        # choose next edge
        for agent in self.agents.values():
            if int(agent.dest) == -1:
                next_node = self.station.get(0).pop(0)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())
                print(self.client.get_pokemons())
                print(self.client.get_agents())

        self.client.move()


def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    t.get_agents()
    t.get_pokemon()
    t.main_loop()







if __name__ == '__main__':
    main()
