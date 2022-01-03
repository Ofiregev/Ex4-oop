import startGame
import DiGraph


class Algo:
    def __init__(self,g:DiGraph):
        self.g = g
        self.graphDict = self.g.graphDict
        self.edges = {}
        for i in self.graphDict.values():
            for j in i.outEdge:
                s = ""
                s = s + str(i.id)+","
                s=s+str(j)

                # list.append(i.id)
                # list.append(j)
                self.edges[s] = self.graphDict.get(i.id).outEdge.get(j)

    ###i want to find on which edge the pokemon is on
    def distance(self,src:str, dst:str):
        if self.edges.get(src,dst) is not None:
            s = self.graphDict.get(int(src))
            d = self.graphDict.get(int(dst))
            x1 = self.g.posGetX(s.pos)
            y1 = self.g.posGetY(s.pos)
            x2 = self.g.posGetX(d.pos)
            y2 = self.g.posGetY(d.pos)
            m = (float(y1)-float(y2))/(float(x1)-float(x2))

        print(m)




def main():
    g = DiGraph.DiGraph()
    t = startGame.startGame(g)
    t.load_json()
    a = Algo(t.get_graph())
    print(a.distance("0","1"))

if __name__ == '__main__':
    main()