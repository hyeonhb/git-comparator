
class IVirtualObject:
    engine = None
    name = None

    def __init__(self, engine, name=""):
        self.engine = engine
        self.name = name
        self.enable() #모든 오브젝트는 생성 시 engine에 등록됨

    def enable(self):
        self.engine.register_object(self)

    def update(self):
        pass

    def disable(self):
        self.engine.unregister_object(self)
    