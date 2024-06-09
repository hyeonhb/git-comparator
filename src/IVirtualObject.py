
class IVirtualObject:
    engine = None
    name = None

    def __init__(self, engine, name=""):
        self.engine = engine
        self.name = name
        pass

    def enable(self):
        self.engine.register_object(self)
        pass

    def update(self):
        pass

    def disable(self):
        self.engine.unregister_object(self)
        pass
    