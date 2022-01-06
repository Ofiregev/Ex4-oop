import json
import math
from types import SimpleNamespace

import Algo
from DiGraph import Node, Edge, DiGraph
from Ex4.client_python import players
from Ex4.client_python.Gui import Gui
from client import Client
from players import pokemon as pok


class startGame:
    def __init__(self, g: DiGraph):
        self.g = g  ## the graph Type: Digraph
        self.algo = Algo.Algo(g)
        self.pokemon = {}
        self.agents = {}
        self.station = {}
        self.value = {}
        # default port
        PORT = 6666
        # server host (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.client.add_agent("{\"id\":9}")
        self.client.add_agent("{\"id\":4}")
        self.client.add_agent("{\"id\":10}")
        self.client.add_agent("{\"id\":0}")

    def load_json(self):

        graph_json = self.client.get_graph()
        graph_obj = json.loads(graph_json)
        nodes = graph_obj["Nodes"]
        edge = graph_obj["Edges"]
        Nodes = []
        Edges = []

        for n in nodes:
            Nodes.append(Node(n))
        for e in edge:
            Edges.append(Edge(e))
        for i in Nodes:
            self.g.add_node(i.id, i.pos)
        for i in Edges:
            self.g.add_edge(i.src, i.dest, i.w)

        self.algo = Algo.Algo(self.g)

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.g

    def get_pokemon(self):
        pokemons_json = self.client.get_pokemons()
        pokemon_obj = json.loads(pokemons_json)
        pokemons = pokemon_obj["Pokemons"]
        # pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            if not self.pokemon.get(p.get("Pokemon").get("pos")):
                w = p.get("Pokemon").get("pos").split(',')
                sr = w[0]
                ds = w[1]
                for i in self.algo.edges:
                    s = i.split(',')
                    src = s[0]
                    dst = s[1]
                    if self.algo.distance(src, dst, sr, ds, p.get("Pokemon").get("type")) is not None:
                        ans = self.algo.distance(src, dst, sr, ds, int(p.get("Pokemon").get("type")))
                        self.pokemon[p.get("Pokemon").get("pos")] = pok(p, ans)
            else:
                if self.pokemon.get(p.get("Pokemon").get("pos")).isDone:
                    self.pokemon.pop(p.get("Pokemon").get("pos"))

    def main_loop(self):
        self.client.start()
        self.get_agents()
        while self.client.is_running() == 'true':
            self.get_agents()
            self.get_pokemon()
            self.next_station()


    def get_agents(self):
        # p.get("Pokemon").get("pos")
        agents_json = self.client.get_agents()
        agents_obj = json.loads(agents_json)
        agents = agents_obj["Agents"]
        for a in agents:
            if self.agents.get(a.get("Agent").get("id")) is None:
                self.agents[a.get("Agent").get("id")] = players.agent(a)
            self.agents.get(a.get("Agent").get("id")).dest = a.get("Agent").get("dest")
            self.agents.get(a.get("Agent").get("id")).info = a
            if float(a.get("Agent").get("speed")) != float(self.agents.get(a.get("Agent").get("id")).speed):
                self.agents.get(a.get("Agent").get("id")).speed = a.get("Agent").get("speed")


    def find_pok(self, agent: players.agent):
        min =  math.inf
        l = []
        pe = None
        for p in self.pokemon.values():
            if not p.taken:
                res = self.algo.shortest_path(agent.info.get("Agent").get("src"), int(p.edge[0]), int(p.edge[1]))
                price = self.algo.min_price(agent, p.value, res[0])
                if min > price:
                    min = price
                    l = res[1]
                    pe = p
        if not l:
            print("shit happend")
            return
        print(f"@@@@ the choise is pokemone value: {pe.value} and the way cost will cost: {min}, the speed of the agent is {agent.speed}")
        l.pop(0)
        pe.taken = True
        agent.pos = pe.pos
        agent.busy = True
        self.station[agent.id] = l
        return res[0]

    def check_catch(self):
        pokemons = json.loads(self.client.get_pokemons(),
                              object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        print(pokemons)
        temp = {}
        for p in pokemons:
            temp[p.pos] = self.pokemon.get(p.pos)
        self.pokemon = temp

    def next_station(self):
            for a in self.agents.values():
                if int(a.dest) == -1:
                    if self.pokemon.get(a.pos):
                        self.pokemon.get(a.pos).taken = False
                    self.check_catch()
                    self.find_pok(a)
                    print("--------------------------------------------------------------------------------")
                    next_node = self.station.get(a.id).pop(0)
                    self.client.choose_next_edge(
                        '{"agent_id":' + str(a.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = self.client.time_to_end()
                    print(ttl, self.client.get_info())
                    pok_list = self.client.get_pokemons()
                    print(pok_list)
                    print([p.info for p in self.pokemon.values()])
                    print(f"the next stations{self.station}")
                    print(self.pokemon.get(a.pos).edge)
                    print(self.client.get_agents())

            self.client.move()




def main():
    g = DiGraph()
    t = startGame(g)
    t.load_json()
    t.get_agents()
    t.get_pokemon()
    Gui(t)



if __name__ == '__main__':
     main()
