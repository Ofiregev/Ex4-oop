import json
from types import SimpleNamespace

import startGame
import DiGraph
from Ex4.client_python.student_code import client


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

                # list.append(i.id)
                # list.append(j)
                self.edges[s] = self.graphDict.get(i.id).outEdge.get(j)




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
            res = y - m * x
            # print(res)
            if c - 0.0001 <= res <= c + 0.0001:
                if type == -1:
                    if src < dst:
                        return dst, src
                    else:
                        return src, dst
                else:
                    if src < dst:
                        return dst, src
                    else:
                        return src, dst

        # print(m)


def main():
    g = DiGraph.DiGraph()
    t = startGame.startGame(g)
    t.load_json()
    a = Algo(t.get_graph())
    ###
    for i in a.edges:
        s = i.split(',')
        src = s[0]
        dst = s[1]
        print(a.distance(src, dst, 35.197656770719604, 32.10191878639921, -1))


if __name__ == '__main__':
    main()
