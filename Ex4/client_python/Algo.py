import startGame
import DiGraph


class Algo:
    def __init__(self,g:DiGraph):
        self.g = g
        self.graphDict = self.g.graphDict
    def distance(self,src:int,dst:int):
        s = self.graphDict.get(src)
        d = self.graphDict.get(dst)
        if not s.outEdge.get(dst):
            return None
