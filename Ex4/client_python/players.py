from types import SimpleNamespace


class pokemon:
    def __init__(self, p: SimpleNamespace, e: list):
        self.info = p
        self.edge = e
        self.taken_by = False
        self.isDone = False


class agent:
    def __init__(self, a: SimpleNamespace):
        self.id = a.id
        self.src = a.src
        self.dest = a.dest
        self.speed = a.speed
        self.info = a
        self.busy = False

    def __str__(self):
        return f"(agent id: {self.id} src: {self.src} dest: {self.dest} speed: {self.speed} busy: {self.busy})"
