from math import inf

import DiGraph
# import startGame
from players import agent


class Algo:
    def __init__(self, g: DiGraph):
        self.g = g
        self.graphDict = self.g.graphDict
        self.edges = {}
        for i in self.graphDict.values():
            for j in i.outEdge:
                s = ""
                s = s + str(i.id) + ","
                s = s + str(j)
                self.edges[s] = self.graphDict.get(i.id).outEdge.get(j)
        self.D = {}  ## dict for calculate dijckstra
        self.nodeQ = []
        self.black = []
        self.parent = {}

    def Dijkstra(self, src: int):

        """finding the sorted path for every src,
        The algo save only the path of one src' in self.D, if we run this for other
        src it will it will change the param on self.D"""
        self.D = {}
        self.nodeQ = []
        self.black = []
        self.parent = {}

        for i in self.g.graphDict:
            if i == src:
                self.nodeQ.append({"id": src, "w": 0})
                self.D[src] = 0
                self.parent[src] = -1
            else:
                self.D[i] = inf  ##save in a dictinury the nodes w ,this is good bebause its by key
        while len(self.black) != len(self.g.graphDict):
            if self.nodeQ.__len__() == 0:
                return
            self.nodeQ = sorted(self.nodeQ, key=lambda i: i['w'])
            v = self.nodeQ.pop(0)['id']
            if (self.black.__contains__(v)):
                continue
            self.black.append(v)
            nei = self.g.getEdgeBySrc(v)
            for i in nei:
                self.relax(v, i)


    def relax(self, v, t):
        curr_w = self.D[v] + self.g.getWeightOfEdge(v, t)
        if self.D[t] > float(curr_w):
            self.D[t] = float(curr_w)
            self.parent[t] = v
            self.nodeQ.append({"id": t, "w": curr_w})

    def shortest_path(self, id1: int, id2: int,dest:int) -> (float, list):
        if  self.g.graphDict.get(id1) is None:
            list = []
            list.append(float('inf'))
            list.append([])
            return list
        self.Dijkstra(id1)
        list1 = []
        list2 = []
        # print(self.g.getWeightOfEdge(id2,dest))
        # print(self.D.get(id2))
        list1.append(self.D.get(id2)+self.g.getWeightOfEdge(id2,dest))
        list3=[]
        i = id2
        while (i != -1 and self.parent.get(i) != -1):
            t = self.parent.get(i)
            list3.append(t)
            i = self.parent.get(i)
        while len(list3) != 0:
            list2.append(list3.pop(len(list3)-1))

        list2.append(id2)
        list2.append(dest)
        list1.append(list2)
        return list1


    def time_to_take(self, speed:float, w:float ):
        return w/speed

    def min_price(self, agent:agent, pok_value,pok_w):
       return pok_value/self.time_to_take(pok_w,agent.speed)



    ###i want to find on which edge the pokemon is on
    def distance(self, src: str, dst: str, x, y, type: int):
        if self.edges.get(src, dst) is not None:
            s = self.graphDict.get(int(src))
            d = self.graphDict.get(int(dst))
            x1 = self.g.posGetX(s.pos)
            y1 = self.g.posGetY(s.pos)
            x2 = self.g.posGetX(d.pos)
            y2 = self.g.posGetY(d.pos)
            m = (float(y1) - float(y2)) / (float(x1) - float(x2))
            c = float(y1) - m * float(x1)
            # print(c)
            res = float(y) - m * float(x)
            # print(res)
            if c - 0.000000000001 <= res <= c + 0.000000000001:
                if type == -1:
                    if src < dst:
                        return dst, src
                else:
                        return src, dst

