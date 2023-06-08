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

import gc
import random
# import timeit
from sys import exit

import bufferables
import pygame
import Character_2D
import Boxes_2D
import Walls

colors = [
    '#5e6f5d', '#42686c',
    '#528387', '#c60018', '#930011',
    '#70B237', '#477A1E', '#ff935e',
    '#854F2B', '#61371F', '#8d8d8d',
    '#818181', '#5d5d5d', '#242526',
    '#cdaa50', '#fdc57a', '#eddcaf'
]


# print(dir(gc))

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

        # Alternate loading state
        self.setUp = True

        # Surface object window is centered on
        self.__screen = pygame.display.set_mode(self.__screenxy) #, pygame.FULLSCREEN)
        self.__screen_rect = self.__screen.get_rect()

        self.__font = pygame.font.Font(None, 32)

        self.__player = Character_2D.Player((100, 100))  # , 'teek')  # plan to add variants that can be accessed here,
        # alternate models or behavior
        self.__player2 = Character_2D.Player((40, 40))

        self.__Boxes_2D_box_list = []

        self.__Wall_list = []

        self.spawnCounter = 1000

        ## debug text on screen
        #  I think storing text elements here even if one of them changes
        #  every frame is faster than both of them being made in-loop.

        self.Box_count_text = self.__font.render(f'Boxes: Unknown', False, colors[0])
        self.Box_count_rect = self.Box_count_text.get_rect(midtop = self.__screen_rect.midtop)



        # loop

    def main(self):
        if self.setUp:
            ## only calls this stem once when triggered. Contents to vary, perhaps this is a standard
            self.setUp = False

            self.__Wall_list.append(Walls.Wall((80, 640), (0, 360), 3)) #LEFT
            self.__Wall_list.append(Walls.Wall((80, 640), (1280, 360), 3)) #RIGHT
            self.__Wall_list.append(Walls.Wall((1200, 80), (640, 0), 3)) #TOP
            self.__Wall_list.append(Walls.Wall((1200, 80), (640, 720), 3)) #BOTTOM

            self.__Wall_list.append(Walls.Wall((150, 50), (350, 350), 3))
            self.__Wall_list.append(Walls.Wall((150, 50), (350, 200), 3))
            self.__Wall_list.append(Walls.Wall((50, 150), (275, 275), 3))


        print('Frame Start')
        # Render background, wipes screen clean each frame
        pygame.draw.rect(self.__screen, 'DarkBlue', (0, 0, self.__screen_rect.width, self.__screen_rect.height))

        ## debug text on screen
        # self.Box_count_text = self.__font.render(f'Boxes: {len(self.__Boxes_2D_box_list)}', False, colors[6])
        # self.__screen.blit(self.Box_count_text, self.Box_count_rect)
        ##

        # bufferables loop
        for bufferObject in self.bufferlist:
            bufferObject.cycle(self.__screen)
            for box in self.__Boxes_2D_box_list:
                # print(f'{bufferObject.get_cloneSurfRect()[1]}')
                if box.rect.colliderect(bufferObject.surfRect[1]):
                    if bufferObject.get_type() == 'laser':
                        bufferObject.DeleteFlag = True
                    if bufferObject.Damaging:
                        box.setDeleteFlag(True)

            if bufferObject.DeleteFlag:
                self.bufferlist.remove(bufferObject)
                del bufferObject

        ## character 2D things
        # / for i in range(4) things. (divide frames by 4 to allow step-wise calculation. This enhances collision de-
        # tection by allowing the objects to move smaller steps to their destination on the next frame.
        self.__player.cycle()
        for i in range(4):
            # calculate movement, choose the control scheme ( there is 'WASD', and 'ARROW' )
            self.__player.movement('WASD')

            # collision with box_2D obect detection
            for box in self.__Boxes_2D_box_list:
                if box.rect.colliderect(self.__player.collider_zone_rect):
                    self.__player.collision(box, self.__Boxes_2D_box_list)
                # if box collides with the player's zone rect? I'm trying something out here
                #     for otherBox in self.__Boxes_2D_box_list:
                #         if box.rect.colliderect(otherBox.collider_zone_rect):
                #             box.collision(otherBox, self.__Boxes_2D_box_list)
                    # Break_case_collision = True
            # self.__player.movement('WASD')
            for wall in self.__Wall_list:
                self.__screen.blit(wall.surf, wall.rect)
                if wall.rect.colliderect(self.__player.collider_zone_rect):
                    self.__player.collision(wall, self.__Wall_list)
                for box in self.__Boxes_2D_box_list:
                    if box.rect.colliderect(wall.rect):
                        box.collision(wall, self.__Wall_list)




                    # show character
        self.__screen.blit(self.__player.surf, self.__player.rect)

        # debug 3 lines visualize colliders
        for collider_rect in self.__player.COLLIDER_RECT_LIST:
            collider_surf = pygame.Surface((collider_rect.w, collider_rect.h))
            # self.__screen.blit(collider_surf, collider_rect)

        # Box 2D things
        for box in self.__Boxes_2D_box_list:
            ## box removal protocol
            if box.DeleteFlag:
                ## randomly pick a death
                # death_anim = []
                # death_anim.append(bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "quadDestruction", (box.surf, box.rect)))
                # death_anim.append(bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "cloneFall", (box.surf, box.rect)))
                # self.bufferlist.append(random.choice(death_anim))

                ## quad destruction death animation
                self.bufferlist.append(
                    bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "quadDestruction",
                                          (box.surf, box.rect)))

                ## clone fall animation
                # self.bufferlist.append(bufferables.animation([box.rect.centerx, box.rect.centery], [0, 0], "cloneFall", (box.surf, box.rect)))

                ## deletion of box, effects are now in the buffer list and object with colliders is gone.
                self.__Boxes_2D_box_list.remove(box)
                # print(self.__Boxes_2D_box_list)
                continue

        for box in self.__Boxes_2D_box_list:
            self.__screen.blit(box.surf, box.rect)

            # debug 3 lines visualize box colliders
            # for collider_rect in box.COLLIDER_RECT_LIST:
            #     collider_surf = pygame.Surface((collider_rect.w, collider_rect.h))
                # self.__screen.blit(collider_surf, collider_rect)

        # Logic
        # print("tick " + str(pygame.time.get_ticks()))

        ''' this will spawn a new batch of boxes with random locations tiled on the screen and not in collision with 
        any other boxes or main player
        '''
        if pygame.time.get_ticks() > self.spawnCounter:
            self.spawnCounter = self.spawnCounter + 1000

            for i in range(20):
                collision = False
                testBox = Boxes_2D.Box((50, 50),
                                       [round(random.randint(100, self.__screen_rect.right - 100) / 50) * 50,
                                        round(random.randint(100, self.__screen_rect.bottom - 100) / 50) * 50],
                                       random.choice(colors))

                for box in self.__Boxes_2D_box_list:
                    if testBox.rect.colliderect(box.rect):
                        collision = True
                ## check player collision
                if testBox.rect.colliderect(self.__player.rect):
                    collision = True

                if not collision:
                    if len(self.__Boxes_2D_box_list) < 0:
                        self.__Boxes_2D_box_list.append(testBox)

        # checking pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.__player.laser(self.bufferlist)

        ## spawn boxes by holding key
        if keys[pygame.K_t]:
            for i in range(20):
                collision = False
                # Bx = Box width
                # By = Box height
                # Bav is the average of Bx and By
                Bx = random.randint(20, 21)
                By = random.randint(20, 21)
                Bav = (Bx + By) / 2

                testBox = Boxes_2D.Box((Bx, By),
                                       [round(random.randint(100, self.__screen_rect.right - 100) / Bav) * Bav,
                                        round(random.randint(100, self.__screen_rect.bottom - 100) / Bav) * Bav],
                                       random.choice(colors))

                for box in self.__Boxes_2D_box_list:
                    if testBox.rect.colliderect(box.rect):
                        collision = True
                if testBox.rect.colliderect(self.__player.rect):
                    collision = True
                for wall in self.__Wall_list:
                    if testBox.rect.colliderect(wall.rect):
                        collision = True

                if not collision:
                    self.__Boxes_2D_box_list.append(testBox)

        # Considers all event types
        for event in pygame.event.get():
            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                # If the key is escape, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    gc.collect()
                    exit()

                if event.key == pygame.K_SPACE:
                    self.__player.punch(self.bufferlist)

                # if event.key == pygame.K_q:
                #     print(gc.DEBUG_UNCOLLECTABLE)
                # if event.key == pygame.K_x:
                #     gc.collect()

                ## spawn boxes with each key press
                if event.key == pygame.K_e:
                    for i in range(1):
                        collision = False
                        ## Bx = Box width
                        ## By = Box height
                        ## Bav is the average of Bx and By
                        # Bx = random.randint(2, 200)
                        # By = random.randint(2, 200)
                        Bx = 10
                        By = 400
                        Bav = (Bx + By) / 2

                        testBox = Boxes_2D.Box((Bx, By),
                                               [round(random.randint(100, self.__screen_rect.right - 100) / Bav) * Bav,
                                                round(
                                                    random.randint(100, self.__screen_rect.bottom - 100) / Bav) * Bav],
                                               random.choice(colors))

                        for box in self.__Boxes_2D_box_list:
                            if testBox.rect.colliderect(box.rect):
                                collision = True
                        if testBox.rect.colliderect(self.__player.rect):
                            collision = True

                        if not collision:
                            self.__Boxes_2D_box_list.append(testBox)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                self.__Boxes_2D_box_list.append(Boxes_2D.Box((80, 80), pygame.mouse.get_pos(), random.choice(colors)))

        pygame.display.update()
        self.__clock.tick(self.__framerate)

        return


if __name__ == '__main__':
    # PrimaryObject = PGConfig((2, 2), 60)
    PrimaryObject = PGConfig((1280, 720), 60)

    # lag_count = 0

    while True:
        # toc = timeit.default_timer()
        # try:
        #     time = toc - tic  # elapsed time in seconds
        # except:
        #     time = 0
        #
        # # print(time)
        # if time > .018:
        #     lag_count = lag_count + 1
        #     print(f'late frames: {lag_count}\n{time}')
        #
        # tic = timeit.default_timer()

        PrimaryObject.main()
