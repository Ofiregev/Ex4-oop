import json
import math
from types import SimpleNamespace

import Algo
from DiGraph import Node, Edge, DiGraph
from Ex4.client_python import players
from client import Client
from players import pokemon as pok


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph
        self.algo = None
        self.pokemon = {}
        self.agents = {}
        self.station = {}
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
            if not self.pokemon.get(p.pos):
                w = p.pos.split(',')
                sr = w[0]
                ds = w[1]
                for i in self.algo.edges:
                    s = i.split(',')
                    src = s[0]
                    dst = s[1]
                    if self.algo.distance(src, dst, sr, ds, p.type) is not None:
                        ans = self.algo.distance(src, dst, sr, ds, int(p.type))
                        self.pokemon[p.pos] = pok(p, ans)
                        print(f"add pokemon, {p}")

    def main_loop(self):
        self.client.start()
        self.get_agents()
        print(99)
        while self.client.is_running() == 'true':
            self.get_agents()
            self.get_pokemon()
            self.next_station()
            # time.sleep(0.1)

    def get_agents(self):
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            if self.agents.get(a.id) is None:
                self.agents[a.id] = players.agent(a)
                print(f"add agent, {a}")
            self.agents.get(a.id).dest = a.dest
            self.agents.get(a.id).info = a
            if float(a.speed) != float(self.agents.get(a.id).speed):
                self.agents.get(a.id).speed = a.speed
                print(f" changing the speed to: {a.speed}")
                continue

    def find_pok(self, agent: players.agent):
        min = math.inf
        l = []
        pe = None
        for p in self.pokemon.values():
            if not p.taken:
                res = self.algo.shortest_path(agent.src, int(p.edge[0]), int(p.edge[1]))
                price = self.algo.min_price(agent, p.value, res[0])
                if min >= price:
                    min = price
                    l = res[1]
                    pe = p
        if not l:
            return
        l.pop(0)
        pe.taken = True
        agent.busy = True
        self.station[agent.id] = l




    def next_station(self):
        for agent in self.agents.values():
            if not agent.busy:
                print("1")
                self.find_pok(agent)
            if agent.dest == -1 and agent.busy and not self.station.get(agent.id):
                print("2")
                agent.busy = False
                self.find_pok(agent)
            if agent.dest == -1 and agent.busy:
                print("3")
                if self.station.get(agent.id):
                    next_node = self.station.get(agent.id).pop(0)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                    agent.dest = agent.info.dest
                    ttl = self.client.time_to_end()
                    print(ttl, self.client.get_info())
                    print(self.client.get_pokemons())
                    print(self.client.get_agents())
                else:
                    print("4")
                    agent.busy = False
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
