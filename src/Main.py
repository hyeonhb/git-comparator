from Display import Display
from VirtualSimEngine import VirtualSimEngine
from CommanderAnt import CommanderAnt

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    engine.stop()