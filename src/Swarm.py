from ISwarm import ISwarm

class Swarm(ISwarm):
    def __init__ (self, position, orientation):
        super().__init__(position, orientation)
        self.swarm_robot_list = []
    
    def add_robot(self, robot):
        pass

    def remove_robot(self, robot):
        pass