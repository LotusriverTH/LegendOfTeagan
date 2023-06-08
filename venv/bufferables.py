
# import pygame
import pygame


class animation:
    def __init__(self, cordinates_xy_list, direction_xy_list, type, cloneSurfRect=()):
        self.__cordinates_xy_list = cordinates_xy_list
        self.__direction_xy_list = direction_xy_list
        self.__type = type
        self.__cloneSurfRect = cloneSurfRect

        self.__surf = pygame.Surface((0,0))
        self.__rect = self.__surf.get_rect()

        self.surfRect = (0,0)

        self.frames = 0
        self.dimensions = [0, 0]

        self.initFlag = True
        self.DeleteFlag = False
        self.Damaging = False

        self.ticker = 0

        self.laser_texture = pygame.image.load('venv/graphics/Attacks/FireBall.png').convert()
        # self.laser_JPG = pygame.transform.scale(self.laser_JPG, self.__rect.size)

    def get_type(self):
        print(self.__type)
        return self.__type

    def get_cloneSurfRect(self):
        return self.__cloneSurfRect

    def punch(self):
        if self.initFlag:
            self.frames = 15
            self.dimensions = [10, 10]
            self.initFlag = False
            self.Damaging = True

        if self.frames:
            self.frames -= 1
            if not self.frames:
                self.DeleteFlag = True
            # print("punching")
            self.dimensions[0] = self.dimensions[0] + 10
            self.dimensions[1] = self.dimensions[1] + 10

            self.__cordinates_xy_list[0] -= round(self.__direction_xy_list[1] / 10)
            self.__cordinates_xy_list[1] -= round(self.__direction_xy_list[0] / 10)


            retSurf = pygame.Surface(self.dimensions)
            retSurf.fill("red")

            return retSurf

    def laser(self):
        if self.initFlag:
            self.frames = 150
            self.dimensions = [40,40]
            self.initFlag = False
            self.Damaging = True
            self.__surf = pygame.Surface(self.dimensions)
            self.__rect = pygame.Surface.get_rect(self.__surf)
            self.laser_texture = pygame.transform.scale(self.laser_texture, self.__rect.size)

        if self.frames:
            self.frames -= 1
            if not self.frames:
                self.DeleteFlag = True

            # print("lasering")
            # print(self.__direction_xy_list)
            self.__cordinates_xy_list[0] -= round(self.__direction_xy_list[1] / 10)
            self.__cordinates_xy_list[1] -= round(self.__direction_xy_list[0] / 10)


            retSurf = pygame.Surface(self.dimensions)
            retSurf.fill("red")

            return retSurf

    def quadDestruction(self):
        if self.initFlag:
            self.frames = 60
            self.initFlag = False
            self.__cordinates_xy_list = self.__cloneSurfRect[1].center
            self.surfRect = self.__cloneSurfRect

        if self.frames:
            # print('quadDestructioning')

            retSurfRect = self.surfRect
            self.frames -= 1


            return retSurfRect

        # print(self.frames)


    def cloneFall(self):
        if self.initFlag:
            self.frames = 50
            self.initFlag = False

        if self.frames:
            self.frames -= 1
            if not self.frames:
                self.DeleteFlag = True

            # print('cloneFalling')
            self.__cordinates_xy_list[1] = self.__cordinates_xy_list[1] + 3
            retSurf = self.__cloneSurfRect[0]

            return retSurf



    def cycle(self, configScreen, cloneSurfRect=False):
        if self.__type == "punch":
            surf = self.punch()
            rect = surf.get_rect(center = self.__cordinates_xy_list)
            configScreen.blit(surf, rect)

        if self.__type == "laser":
            surf = self.laser()
            rect = surf.get_rect(center = self.__cordinates_xy_list)
            configScreen.blit(self.laser_texture, rect)

        if self.__type == "cloneFall":
            surf = self.cloneFall()
            rect = surf.get_rect(center = self.__cordinates_xy_list)
            configScreen.blit(surf, rect)

        if self.__type == "quadDestruction":
            if self.initFlag:
                self.frames = True

            if self.frames:
                self.ticker = self.ticker + 1
                pre_surfRect = self.quadDestruction()
                pre_surf1 = pre_surfRect[0]
                pre_rect1 = pre_surfRect[1]
                surf1 = pygame.transform.scale(pre_surf1, [pre_rect1.w/2, pre_rect1.h/2])
                rect1 = surf1.get_rect(bottomright = self.__cordinates_xy_list)


                pre_surfRect = self.quadDestruction()
                pre_surf2 = pre_surfRect[0]
                pre_rect2 = pre_surfRect[1]
                surf2 = pygame.transform.scale(pre_surf2, [pre_rect2.w/2, pre_rect2.h/2])
                rect2 = surf2.get_rect(bottomleft = self.__cordinates_xy_list)


                pre_surfRect = self.quadDestruction()
                pre_surf3 = pre_surfRect[0]
                pre_rect3 = pre_surfRect[1]
                surf3 = pygame.transform.scale(pre_surf3, [pre_rect3.w/2, pre_rect3.h/2])
                rect3 = surf3.get_rect(topright = self.__cordinates_xy_list)


                pre_surfRect = self.quadDestruction()
                pre_surf4 = pre_surfRect[0]
                pre_rect4 = pre_surfRect[1]
                surf4 = pygame.transform.scale(pre_surf4, [pre_rect4.w/2, pre_rect4.h/2])
                rect4 = surf4.get_rect(topleft = self.__cordinates_xy_list)

                rect1.x = rect1.x - (self.ticker*3)
                rect1.y = rect1.y - (self.ticker*3)
                rect2.x = rect2.x + (self.ticker*3)
                rect2.y = rect2.y - (self.ticker*3)
                rect3.x = rect3.x - (self.ticker*3)
                rect3.y = rect3.y + (self.ticker*3)
                rect4.x = rect4.x + (self.ticker*3)
                rect4.y = rect4.y + (self.ticker*3)

                configScreen.blit(surf1, rect1)
                configScreen.blit(surf2, rect2)
                configScreen.blit(surf3, rect3)
                configScreen.blit(surf4, rect4)

                surf = surf1
                rect = rect1

            else:
                surf = pygame.surface.Surface([0,0])
                rect = surf.get_rect(center = [-1000, -1000])

                self.DeleteFlag = True

        surfRect = (surf, rect)
        self.surfRect = surfRect

        return surfRect