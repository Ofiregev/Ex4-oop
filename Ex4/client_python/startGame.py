import json
import time
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

                        print(self.pokemon.get(p.pos).edge)

    def main_loop(self):
        self.client.start()
        self.get_agents()
        t = 200
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.get_agents()
            self.get_pokemon()
            self.next_station()
            time.sleep(0.1)
            # print(timer, end="\r")
            # time.sleep(1)
            t -= 1
        # self.client.start()
        # while self.client.is_running() == 'true':
        #     self.get_agents()
        #     self.get_pokemon()
        #     self.next_station()
        #     time.sleep(0.1)

    def get_agents(self):
        agents = json.loads(self.client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for a in agents:
            self.agents[a.id] = players.agent(a)
            if self.station.get(a.id) is not None:
                a.alloc = True
            # self.station[a.id] = []
            # print(self.agents[a.id])

    def next_station(self):
        # choose next edge
        min = 10000
        list1 = []
        for agent in self.agents.values():
            if agent.dest == -1 and not agent.busy:
                # if agent.alloc == True and len(self.station.get(agent.id))!=0 :
                #         next_node = self.station.get(agent.id).pop(0)
                #         self.client.choose_next_edge(
                #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                #         agent.dest = next_node
                #         print(ttl, self.client.get_info())
                #         print(self.client.get_pokemons())
                #         print(self.client.get_agents())
                #         print(agent)
                #         self.client.move()
                #
                # else:
                choose = pok
                for p in self.pokemon.values():
                    if p.taken:
                        continue
                    w = (self.algo.shortest_path(agent.src, int(p.edge[0]), int(p.edge[1])))
                    # print(w)
                    res = self.algo.min_price(agent, p.value, w[0])
                    if min >= res:
                        min = res
                        choose = self.pokemon.get(p.pos)
                        list1 = w
                    # print(list1)
                # l =self.algo.shortest_path(agent.src,int(choose.edge[0]),int(choose.edge[1]))
                # print(list1[1])
                # list1[1].pop(0)
                self.station[agent.id] = list1[1]
                self.agents.get(agent.id).alloc = True
                self.station.get(agent.id).pop(0)
                next_node = self.station.get(agent.id).pop(0)
                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                agent.dest = next_node
                self.agents.get(agent.id).busy = True
                self.pokemon.get(choose.pos).taken = True

                ttl = self.client.time_to_end()
                print(ttl, self.client.get_info())
                # print(self.client.get_pokemons())
                # print(self.client.get_agents())
                print(agent)
                # print(self.agents.get(agent.id))
            self.client.move()

        # for agent in self.agents.values():
        #     if int(agent.dest) == -1:
        #         next_node = self.station.get(0).pop(0)
        #         self.client.choose_next_edge(
        #             '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
        #         ttl = self.client.time_to_end()
        # print(ttl, self.client.get_info())
        # print(self.client.get_pokemons())
        # print(self.client.get_agents())


def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    t.get_agents()
    t.get_pokemon()
    t.main_loop()


if __name__ == '__main__':
    main()
