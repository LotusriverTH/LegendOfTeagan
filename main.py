'''
Teagan's Attempt at making a zelda-like game from his head. I have been inspired by tile map examples as well as
state stacking theory for game dev. I will be using pygame to at least make

chests that open and tell you what you got [ ]
an inventory [ ]
some sort of 2d array for saving tile info/color [ ]
                    (Bonus: two surfaces in one spot?) [ ]
enemies to swipe at with weapon and die [ ]
multiple weapons with unique frames, using weapon framework [x]

( These all feel a tad lofty, but if there are any "X"s in those boxes then know I tried!)
'''

## BERTO! The controls are:
#       WASD --
#       Space -- (Press to 'punch', hold to fire 'lasers')
#       E -- populate screen with more squares
#       Any mouse button -- place square at pointer location

# LMK if you have any questions, I kind of struggle to modify this sometimes but I understand it pretty well

import random
from sys import exit

import bufferables
import pygame
import Character_2D
import Boxes_2D

colors = [
'#5e6f5d','#42686c',
'#528387','#c60018','#930011',
'#70B237','#477A1E','#ff935e',
'#854F2B','#61371F','#8d8d8d',
'#818181','#5d5d5d','#242526',
'#cdaa50','#fdc57a','#eddcaf'
]



class PGConfig:
    def __init__(self, screenxy, framerate):
        self.__screenxy = screenxy
        self.__framerate = framerate
        self.bufferlist = []

        # Main game engine
        pygame.init()

        # Tick rate engine
        self.__clock = pygame.time.Clock()

        # Window Name
        pygame.display.set_caption("Legend Of Teagan")

        # Surface object window is centered on
        self.__screen = pygame.display.set_mode(self.__screenxy)
        self.__screen_rect = self.__screen.get_rect()

        self.__player = Character_2D.Player((100, 100))# , True)  # load in separate character controller
        self.__Boxes_2D_box_list = []

        self.spawnCounter = 1000


        # loop
    def main(self):
        # Render background, wipes screen clean each frame
        pygame.draw.rect(self.__screen, 'DarkBlue', (0, 0, self.__screen_rect.width, self.__screen_rect.height))
        Box_count_surf = pygame.font.Font(None, 50).render(f'Boxes: {len(self.__Boxes_2D_box_list)}', False, colors[0])
        Box_count_rect = Box_count_surf.get_rect(topleft = self.__screen_rect.topleft)
        self.__screen.blit(Box_count_surf, Box_count_rect)

        # bufferables loop
        for bufferObject in self.bufferlist:
            bufferedSurfRect = bufferObject.cycle(self.__screen)
            for box in self.__Boxes_2D_box_list:
                if box.rect.colliderect(bufferedSurfRect[1]):
                    if bufferObject.Damaging:
                        box.setDeleteFlag(True)

            if bufferObject.DeleteFlag:
                self.bufferlist.remove(bufferObject)


        # character 2D things
        self.__screen.blit(self.__player.surf, self.__player.rect)
        self.__player.movement('WASD')
        for box in self.__Boxes_2D_box_list:
            x = box.rect
            self.__player.collision(x)
        # self.__player.movement('ARROW')
        # print(f'X = {self.__player.speed[0]}\nY = {self.__player.speed[1]}')

        # Box 2D things
        for box in self.__Boxes_2D_box_list:
            if box.DeleteFlag:
                self.bufferlist.append(bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "quadDestruction", (box.surf, box.rect)))
                # self.bufferlist.append(bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "cloneFall", (box.surf, box.rect)))
                self.__Boxes_2D_box_list.remove(box)

            for boxclone in self.__Boxes_2D_box_list:
                box.collision(boxclone.rect)
        for box in self.__Boxes_2D_box_list:
            self.__screen.blit(box.surf, box.rect)

        # Logic
        # print("tick " + str(pygame.time.get_ticks()))


        if pygame.time.get_ticks() > self.spawnCounter:
            self.spawnCounter+= 1000
            for i in range(20):
                collision = False
                testBox = Boxes_2D.Box((50, 50),
                                       [round(random.randint(100, self.__screen_rect.right - 100) / 50) * 50,
                                        round(random.randint(100, self.__screen_rect.bottom - 100) / 50) * 50],
                                       random.choice(colors))

                for box in self.__Boxes_2D_box_list:
                    if testBox.rect.colliderect(box.rect):
                        collision = True
                if testBox.rect.colliderect(self.__player.rect):
                    collision = True

                if not collision:
                    if len(self.__Boxes_2D_box_list)<10:
                        self.__Boxes_2D_box_list.append(testBox)




        # checking pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.__player.laser(self.bufferlist)

        # Considers all event types
        for event in pygame.event.get():
            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                # If the key is escape, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

                if event.key == pygame.K_SPACE:
                    self.__player.punch(self.bufferlist)

                # if event.key == pygame.K_q:
                #     self.__player.laser(self.bufferlist)

                if event.key == pygame.K_e:

                    for i in range(20):
                        collision = False
                        testBox = Boxes_2D.Box((50, 50),
                                                [round(random.randint(100, self.__screen_rect.right-100)/50)*50,
                                                round(random.randint(100, self.__screen_rect.bottom-100)/50)*50], random.choice(colors))

                        for box in self.__Boxes_2D_box_list:
                            if testBox.rect.colliderect(box.rect):
                                collision = True
                        if testBox.rect.colliderect(self.__player.rect):
                            collision = True


                        if not collision:
                            self.__Boxes_2D_box_list.append(testBox)


            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                self.__Boxes_2D_box_list.append(Boxes_2D.Box((50, 50), pygame.mouse.get_pos(), random.choice(colors)))

        pygame.display.update()
        self.__clock.tick(self.__framerate)

        return


if __name__ == '__main__':
    PrimaryObject = PGConfig((1280, 720), 60)

    while True:
        PrimaryObject.main()
