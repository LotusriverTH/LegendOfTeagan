import bufferables
import pygame
from math import cos, sin, pi

print('Character_2D Starting')


class Player:
    def __init__(self, size): #, model):
        self.__size = size
        # self.__model = model

        # Set Variables
        self.COLOR = '#C60018'
        self.SPEED_INCREASE_RATE = 2
        self.SPEED_DECREASE_RATE = 1
        self.SPEED_CAP = 16
        self.PUSH_DISTANCE = 5
        self.EFFECTIVE_MAX_SPEED = self.SPEED_CAP - self.SPEED_DECREASE_RATE

        self.attack_range = round(self.__size[0] * .8)
        self.attack_thickness = round(self.__size[0] * .8)

        # Dynamic variables
        self.speed = [0, 0]
        self.degrees = 0
        self.attack_direction = [0, 0]


        # Lists
        self.COLLIDER_RECT_LIST = []

        # player outline object, edges define where the collider objects will go
        # self.surf = pygame.Surface((self.__size[0], self.__size[1]))
        self.png = pygame.image.load('graphics/Teak/Push_1.png').convert_alpha()
        # self.png = pygame.image.load('graphics/Legacygraphics/custom/shell2.png').convert_alpha()
        # self.gif = pygame.image.load('graphics/Helicopter/Helicopter.gif').convert_alpha()
        self.surf_default = pygame.transform.scale(self.png, (self.__size[0], self.__size[1]))
        self.surf = self.surf_default
        # self.surf.fill(self.COLOR)
        self.rect = self.surf.get_rect(center=(200, 200))

        # define collider sizes
        collider_longx = self.__size[0] * .9
        collider_shortx = self.__size[0] * .1

        collider_longy = self.__size[1] * .9
        collider_shorty = self.__size[1] * .1

        # Create collider objects
        self.collider_top_surf = pygame.Surface((collider_longx, collider_shortx))
        self.collider_top_rect = self.collider_top_surf.get_rect(midtop=self.rect.midtop)

        self.collider_bottom_surf = pygame.Surface((collider_longx, collider_shortx))
        self.collider_bottom_rect = self.collider_bottom_surf.get_rect(midbottom=self.rect.midbottom)

        self.collider_left_surf = pygame.Surface((collider_shorty, collider_longy))
        self.collider_left_rect = self.collider_left_surf.get_rect(midleft=self.rect.midleft)

        self.collider_right_surf = pygame.Surface((collider_shorty, collider_longy))
        self.collider_right_rect = self.collider_right_surf.get_rect(midright=self.rect.midright)

        # add colliders' rects to collider_rect_list
        self.COLLIDER_RECT_LIST.append(self.collider_top_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_bottom_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_left_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_right_rect)

    def movement(self, controls):
        # gathers all pressed keys
        keys = pygame.key.get_pressed()
        if controls == 'WASD':
            up = keys[pygame.K_w]
            down = keys[pygame.K_s]
            left = keys[pygame.K_a]
            right = keys[pygame.K_d]

        elif controls == 'ARROW':
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]

        else:
            up = False
            down = False
            left = False
            right = False

        # Left movement
        if left:
            self.surf = pygame.transform.rotate(self.surf_default, 90)
            self.degrees = 90

            self.speed[0] -= self.SPEED_INCREASE_RATE
            if self.speed[0] < -self.SPEED_CAP:
                self.speed[0] = -self.SPEED_CAP
        # Right movement
        if right:
            self.surf = pygame.transform.rotate(self.surf_default, 270)
            self.degrees = 270

            self.speed[0] += self.SPEED_INCREASE_RATE
            if self.speed[0] > self.SPEED_CAP:
                self.speed[0] = self.SPEED_CAP
        # Up movement
        if up:
            self.surf = self.surf_default
            self.degrees = 0

            self.speed[1] -= self.SPEED_INCREASE_RATE
            if self.speed[1] < -self.SPEED_CAP:
                self.speed[1] = -self.SPEED_CAP
        # Down movement
        if down:
            self.surf = pygame.transform.rotate(self.surf_default, 180)
            self.degrees = 180

            self.speed[1] += self.SPEED_INCREASE_RATE
            if self.speed[1] > self.SPEED_CAP:
                self.speed[1] = self.SPEED_CAP

        if up and right:
            self.surf = pygame.transform.rotate(self.surf_default, 315)
            self.degrees = 315

        elif up and left:
            self.surf = pygame.transform.rotate(self.surf_default, 45)
            self.degrees = 45

        elif down and right:
            self.surf = pygame.transform.rotate(self.surf_default, 225)
            self.degrees = 225

        elif down and left:
            self.surf = pygame.transform.rotate(self.surf_default, 135)
            self.degrees = 135

        # x axis speed decrease
        if self.speed[0] < 0:
            self.speed[0] += self.SPEED_DECREASE_RATE
        if self.speed[0] > 0:
            self.speed[0] -= self.SPEED_DECREASE_RATE
        if -self.SPEED_DECREASE_RATE+1 <= self.speed[0] <= self.SPEED_DECREASE_RATE-1:
            self.speed[0] = 0

        # y axis speed decrease
        if self.speed[1] < 0:
            self.speed[1] += self.SPEED_DECREASE_RATE
        if self.speed[1] > 0:
            self.speed[1] -= self.SPEED_DECREASE_RATE
        if -self.SPEED_DECREASE_RATE+1 <= self.speed[1] <= self.SPEED_DECREASE_RATE-1:
            self.speed[1] = 0

        if self.speed[0]>6 and self.speed[1]>6:
            self.speed[0] = round(self.speed[0] / 1.5)
            self.speed[1] = round(self.speed[1] / 1.5)

        if self.speed[0]<-6 and self.speed[1]<-6:
            self.speed[0] = round(self.speed[0] / 1.5)
            self.speed[1] = round(self.speed[1] / 1.5)

        if self.speed[0]<-6 and self.speed[1]>6:
            self.speed[0] = round(self.speed[0] / 1.5)
            self.speed[1] = round(self.speed[1] / 1.5)

        if self.speed[0]>6 and self.speed[1]<-6:
            self.speed[0] = round(self.speed[0] / 1.5)
            self.speed[1] = round(self.speed[1] / 1.5)

        # Apply the calculated movement
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.speed[0] or self.speed[1] != 0:
            self.attack_direction = [
                round(cos(self.degrees * pi / 180) * self.attack_range),
                round(sin(self.degrees * pi / 180) * self.attack_range)
            ]
            # print("Attack Direction: ", self.attack_direction)

        # Place colliders in the proper place on player after they move
        self._moveColliders()

    def movementMOUSE(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.centerx = mouse_pos[0]
        self.rect.centery = mouse_pos[1]

        self._moveColliders()

    def collision(self, rect):
            # Top collision
            if self.collider_top_rect.bottom + 10 > rect.bottom:
                if self.collider_top_rect.colliderect(rect):
                    self.rect.top = rect.bottom
                    self.speed[1] = 0
                    self._push(rect, (0, -self.PUSH_DISTANCE))

            # Bottom collision
            if self.collider_bottom_rect.top - 10 < rect.top:
                if self.collider_bottom_rect.colliderect(rect):
                    self.rect.bottom = rect.top
                    self.speed[1] = 0
                    self._push(rect, (0, self.PUSH_DISTANCE))


            # Left collision
            if self.collider_left_rect.right + 10 > rect.right:
                if self.collider_left_rect.colliderect(rect):
                    self.rect.left = rect.right
                    self.speed[0] = 0
                    self._push(rect, (-self.PUSH_DISTANCE, 0))


            # Right collision
            if self.collider_right_rect.left - 10 < rect.left:
                if self.collider_right_rect.colliderect(rect):
                    self.rect.right = rect.left
                    self.speed[0] = 0
                    self._push(rect, (self.PUSH_DISTANCE, 0))

    def punch(self, configBufferList):
        x_surf = pygame.Surface((self.attack_range, self.attack_thickness))
        x_rect = x_surf.get_rect(center=[self.rect.centerx - self.attack_direction[1], self.rect.centery - self.attack_direction[0]])

        configBufferList.append(bufferables.animation([x_rect.centerx, x_rect.centery], self.attack_direction, "punch"))


    def laser(self, configBufferList):
        x_surf = pygame.Surface((self.attack_range, self.attack_thickness))
        x_rect = x_surf.get_rect(center=[self.rect.centerx - self.attack_direction[1], self.rect.centery - self.attack_direction[0]])

        configBufferList.append(bufferables.animation([x_rect.centerx, x_rect.centery], self.attack_direction, "laser"))




    def _push(self, rect, push_coord):
        rect.x += push_coord[0]
        rect.y += push_coord[1]

    def _moveColliders(self):
        self.collider_top_rect.midtop = self.rect.midtop
        self.collider_bottom_rect.midbottom = self.rect.midbottom
        self.collider_left_rect.midleft = self.rect.midleft
        self.collider_right_rect.midright = self.rect.midright





print('Character_2D Complete')
