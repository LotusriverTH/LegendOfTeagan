import pygame
import bufferables

class Wall:
    def __init__(self, dimensions, location, HP):
        self.__dimensions = dimensions
        self.__location = location
        self.__HP = HP
        self.type = 'wall'

        # Set Variables
        self.COLOR = '#851ca6'

        self.surf = pygame.Surface(dimensions)
        self.surf.fill(self.COLOR)
        self.rect = self.surf.get_rect(center=location)

    def setHP(self, HP):
        self.__HP = self.__HP + HP

    def getHP(self):
        x = 0 + self.__HP
        return x