from Vector3D import Vector3D

class ISwarm:
    def __init__(self,position=Vector3D(0.0, 0.0, 0.0), orientation=Vector3D(0.0, 0.0, 0.0)):
        self.position = position
        self.orientation = orientation

    def rotate(self):
        pass
    
    def move(self):
        pass
    
    def stop(self):
        pass