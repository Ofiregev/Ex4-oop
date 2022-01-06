from types import SimpleNamespace


class pokemon:
    def __init__(self, p, e: list):
        self.info = p
        self.value = p.get("Pokemon").get("value")
        self.pos = p.get("Pokemon").get("pos")
        self.edge = e
        self.type = p.get("Pokemon").get("type")
        self.taken = False
        self.isDone = False

    def __str__(self):
        return f"(pokemon value: {self.value} pos: {self.pos} edge: {self.edge} taken: {self.taken} isDone: {self.isDone})"


class agent:
    def __init__(self, a):
        self.id = a.get("Agent").get("id")
        self.src = a.get("Agent").get("src")
        self.dest = a.get("Agent").get("dest")
        self.speed = a.get("Agent").get("speed")
        self.info = a
        self.busy = False
        self.pos = 0

    def __str__(self):
        return str(self.info)
            # f"(agent id: {self.id} src: {self.src} dest: {self.dest} speed: {self.speed} busy: {self.busy} )"
