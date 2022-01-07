# import copy
# import json
# import timeit
# from math import inf
#
# import Gui
# from DiGraph import Node, Edge, DiGraph
#
#
# class GraphAlgo:
#     def __init__(self,g:DiGraph):
#         self.g = g  ## the graph Type: Digraph
#         self.D = {}  ## dict for calculate dijckstra
#         self.nodeQ = []
#         self.black = []
#         self.parent = {}
#         self.isCo ={}
#
#     def get_graph(self) -> DiGraph:
#         """
#         :return: the directed graph on which the algorithm works on.
#         """
#         return self.g
#
#     def load_from_json(self, Filename: str) -> bool:
#         """
#         Loads a graph from a json file.
#         @param file_name: The path to the json file
#         @returns True if the loading was successful, False o.w.
#         """
#         try:
#             f = open(Filename, 'r')
#         except IOError:
#             return False
#         with f as w:
#             obj = json.load(w)
#             nodes = obj["Nodes"]
#             edge = obj["Edges"]
#             Nodes = []
#             Edges = []
#         for n in nodes:
#             Nodes.append(Node(n))
#         for e in edge:
#             Edges.append(Edge(e))
#         for i in Nodes:
#             self.g.add_node(i.id, i.pos)
#         for i in Edges:
#             self.g.add_edge(i.src, i.dest, i.w)
#
#         return True
#
#     def save_to_json(self, file_name: str) -> bool:
#         nd = []
#         ed = []
#         for key in self.g.graphDict.keys():
#             nd.append({"id": key,
#                        "pos": self.g.graphDict[key].pos})
#             for e in self.g.graphDict[key].outEdge:
#                 ed.append({"src": key, "w": self.g.graphDict[key].outEdge[e], "dest": e})
#         dic = {}
#         dic["Nodes"] = nd
#         dic["Edges"] = ed
#         json_object = json.dumps(dic)
#         try:
#             f = open(file_name, 'w')
#         except IOError:
#             return False
#         f.write(json_object)
#         f.close()
#         # with f as outFile:
#         #     outFile.write(json_object)
#         #     outFile.close()
#         return True
#
#     def TSP(self, node_lst: list[int]) -> (list[int], float):
#         """Greedy Alogorithem - serch for every premutetaion what is the best start node to build shortest path from it"""
#         min = inf
#         """this is the Global min for all the permutations"""
#         lst = []
#         """this lst will represent the most better permutation of the list"""
#         for i in node_lst:
#             """checking when every node is the beginning of the circle what is the most good permutation"""
#             temp = self.find_way(copy.deepcopy(node_lst), i)
#             if temp[1] < min:
#                 min = temp[1]
#                 lst = temp[0]
#         return [lst, min]
#
#     def find_way(self, lst: list, start: int):
#         """"help to TSP function' calculate for every start node the best Circle permute! """
#         per = []
#         per.append(start)
#         lst.remove(start)
#         index = 0
#         w = 0
#         nex = start
#         while lst:
#             self.Dijkstra(nex)
#             min = self.D.get(lst[0])
#             for e in lst:
#                 if self.D.get(e) <= min:
#                     min = self.D.get(e)
#                     index = e
#             nex = index
#             lst.remove(nex)
#             per.append(nex)
#             w += min
#         per.append(start)
#         self.Dijkstra(nex)
#         w += self.D.get(start)
#
#         return [per, w]
#
#     def Dijkstra(self, src: int):
#
#         """finding the sorted path for every src,
#         The algo save only the path of one src' in self.D, if we run this for other
#         src it will it will change the param on self.D"""
#         self.D = {}
#         self.nodeQ = []
#         self.black = []
#         self.parent = {}
#         self.D["maxPath"] = float(-inf)
#         for i in self.g.graphDict:
#             if i == src:
#                 self.nodeQ.append({"id": src, "w": 0})
#                 self.D[src] = 0
#                 self.parent[src] = -1
#             else:
#                 self.D[i] = inf  ##save in a dictinury the nodes w ,this is good bebause its by key
#         while len(self.black) != len(self.g.graphDict):
#             if self.nodeQ.__len__() == 0:
#                 return
#             self.nodeQ = sorted(self.nodeQ, key=lambda i: i['w'])
#             v = self.nodeQ.pop(0)['id']
#             if (self.black.__contains__(v)):
#                 continue
#             self.black.append(v)
#             nei = self.g.getEdgeBySrc(v)
#             for i in nei:
#                 self.relax(v, i)
#         for i in self.g.graphDict:
#             if self.D[i] > self.D["maxPath"]:
#                 self.D["maxPath"] = self.D[i]
#
#     def relax(self, v, t):
#         curr_w = self.D[v] + self.g.getWeightOfEdge(v, t)
#         if self.D[t] > float(curr_w):
#             self.D[t] = float(curr_w)
#             self.parent[t] = v
#             self.nodeQ.append({"id": t, "w": curr_w})
#
#     def shortest_path(self, id1: int, id2: int, dest: int) -> (float, list):
#         if self.g.graphDict.get(id1) is None:
#             list = []
#             list.append(float('inf'))
#             list.append([])
#             return list
#         self.Dijkstra(id1)
#         list1 = []
#         list2 = []
#         # print(self.g.getWeightOfEdge(id2,dest))
#         # print(self.D.get(id2))
#         list1.append(self.D.get(id2) + self.g.getWeightOfEdge(id2, dest))
#         list3 = []
#         i = id2
#         while (i != -1 and self.parent.get(i) != -1):
#             t = self.parent.get(i)
#             list3.append(t)
#             i = self.parent.get(i)
#         while len(list3) != 0:
#             list2.append(list3.pop(len(list3) - 1))
#
#         list2.append(id2)
#         list2.append(dest)
#         list1.append(list2)
#         return list1
#
#     def centerPoint(self) -> (int, float):
#         try:
#             """find the node that have the min wight to move to all the other Nodes"""
#             MAXLIST = {}
#             minMaxPath = float(inf)
#             node_id = -1
#             for i in self.g.graphDict.keys():
#                 self.Dijkstra(i)
#                 MAXLIST[i] = self.D.get("maxPath")
#                 if self.D.get("maxPath") < minMaxPath:
#                     minMaxPath = self.D.get("maxPath")
#                     node_id = i
#             list = []
#             list.append(node_id)
#             list.append(minMaxPath)
#             # print(MAXLIST)
#             # print(MAXLIST.get(362))
#             return list
#         except:
#             list = [None, float(inf)]
#             return list
#
#     def plot_graph(self) -> None:
#         """show the graphic Properties of our DiGraph"""
#         f = Gui.gui
#         f.__init__(f, self)
#
# def main():
#     d = GraphAlgo()
#     file = '../data/A0.json'
#     d.load_from_json(file)
#     start = timeit.default_timer()
#     d.centerPoint()
#     d.plot_graph()
#     stop = timeit.default_timer()
#     print('Time: ', stop - start)
#
# if __name__ == '__main__':
#     main()
