class ICommander:
    def __init__(self, swarm_list):
        self.swarm_list = swarm_list

    def add_swarm(self, swarm):
        self.swarm_list.append(swarm)

    def remove_swarm(self, swarm):
        self.swarm_list.remove(swarm)

    def commander_init(self):
        pass
    def commander_start(self):
        pass
    def commander_pause(self):
        pass
    def commander_play(self):
        pass
    def commander_stop(self):
        pass