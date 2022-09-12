'''
Teagan's Attempt at making a zelda-like game from his head. I have been inspired by tile map examples as well as
state stacking theory for game dev. I will be using pygame to at least make

chests that open and tell you what you got [ ]
an inventory [ ]
some sort of 2d array for saving tile info/color [ ]
                    (Bonus: two surfaces in one spot?) [ ]
enemies to swipe at with weapon and die [ ]
multiple weapons with unique frames, using weapon framework [ ]

( These all feel a tad lofty, but if there are any "X"s in those boxes then know I tried!)
'''

from sys import exit
import pygame
import Character_2D
import Boxes_2D


class PGConfig:
    def __init__(self, screenxy, framerate):
        self.__screenxy = screenxy
        self.__framerate = framerate

        # Main game engine
        pygame.init()

        # Tick rate engine
        self.__clock = pygame.time.Clock()

        # Window Name
        pygame.display.set_caption("Legend Of Teagan")

        # Surface object window is centered on
        self.__screen = pygame.display.set_mode(self.__screenxy)
        self.__screen_rect = self.__screen.get_rect()

        self.__player = Character_2D.Player((50, 50))  # load in separate character controller
        self.__Boxes_2D_box_list = []


        # loop
    def main(self):


        # Render background, wipes screen clean each frame
        pygame.draw.rect(self.__screen, 'DarkBlue', (0, 0, self.__screen_rect.width, self.__screen_rect.height))

        # character 2D things
        self.__screen.blit(self.__player.surf, self.__player.rect)
        self.__player.movement('WASD')
        for box in self.__Boxes_2D_box_list:
            x = box.rect
            self.__player.collision(x)
        # self.__player.movement('ARROW')
        # print(f'X = {self.__player.speed[0]}\nY = {self.__player.speed[1]}')

        # Box 2D things
        for box1 in self.__Boxes_2D_box_list:
            for box2 in self.__Boxes_2D_box_list:
                box1.collision(box2.rect)
        for box in self.__Boxes_2D_box_list:
            self.__screen.blit(box.surf, box.rect)

        # Considers all event types
        for event in pygame.event.get():
            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                # If the key is escape, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__Boxes_2D_box_list.append(Boxes_2D.Box((50, 50), pygame.mouse.get_pos(), 'green'))

        pygame.display.update()
        self.__clock.tick(self.__framerate)

        return


if __name__ == '__main__':
    PrimaryObject = PGConfig((1280, 720), 60)

    while True:
        PrimaryObject.main()
