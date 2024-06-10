from Vector3D import Vector3D

class ISwarm:
    def __init__(self,position=Vector3D(), orientation=Vector3D()):
        self.position = position
        self.orientation = orientation

    def rotate(self, angular_velocity):
        pass
    
    def move(self, velocity):
        pass
    
    def stop(self):
        pass