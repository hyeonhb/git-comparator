import pygame as pg
class Display:
    def __init__(self, width, height, fps, name):
        pg.init()
        self.screen_width = width
        self.screen_height = height
        self.fps = fps
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption(name)
        self.clock = pg.time.Clock()        
        pass

    def start(self, controller):
        try:
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    self.screen.fill((255, 255, 255))
                    pg.display.flip()
                    self.clock.tick(self.fps)
        finally:
            pg.quit()        

        