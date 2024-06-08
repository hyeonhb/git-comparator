class Controller:
    def __init__(self, commander_list):
        self.commander_list = commander_list

    def add_commander(self, commander):
        self.commander_list.append(commander)

    def remove_commander(self, commander):
        self.commander_list.remove(commander)
