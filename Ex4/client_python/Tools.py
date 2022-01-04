from types import SimpleNamespace


class pokemon:
    def __init__(self,p:SimpleNamespace, e:list):
        self.info = p
        self.edge = e
        self.taken_by = False
        self.isDone = False

class agent:
    def __init__(self, a:SimpleNamespace):
        self.id = a.id
        self.info = a
        self.busy = False