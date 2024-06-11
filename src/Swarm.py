from ISwarm import ISwarm
from Vector3D import Vector3D

class Swarm(ISwarm):
    def __init__ (self, position=Vector3D(), orientation=Vector3D()):
        super().__init__(position, orientation)
        self.swarm_robot_list = []
    
    def add_robot(self, robot):
        self.swarm_robot_list.append(robot)
        print("Add robot")
        self.calculate_swarm_center()

    def remove_robot(self, robot):
        if robot in self.swarm_robot_list:
            self.swarm_robot_list.remove(robot)
            print("Remove robot")
            self.calculate_swarm_center()

    def get_robot_list(self):
        return self.swarm_robot_list.copy()

    def calculate_swarm_center(self):
        position_sum = Vector3D()
        for robot in self.swarm_robot_list:
            position_sum = position_sum + robot.position
        self.position = position_sum / len(self.swarm_robot_list)

    def rotate(self, angular_velocity):
        for robot in self.swarm_robot_list:
            robot.rotate(angular_velocity)


    def move(self, velocity):
        for robot in self.swarm_robot_list:
            robot.move(velocity)

    def stop(self):
        for robot in self.swarm_robot_list:
            robot.stop()
        