from Display import Display
from VirtualSimEngine import VirtualSimEngine
from CommanderAnt import CommanderAnt

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    commander = CommanderAnt([])
    commander.commander_start()
    next_velocity = commander.set_next_velocity()
    print('!!! next_velocity:', next_velocity)

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    engine.stop()