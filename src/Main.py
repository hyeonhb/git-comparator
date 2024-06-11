from Display import Display
from VirtualSimEngine import VirtualSimEngine
from CommanderAnt import CommanderAnt

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    commander = CommanderAnt([])
    next_position = commander.get_next_position_list()
    print('!!! next_position:', next_position)

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    engine.stop()