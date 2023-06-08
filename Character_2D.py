import bufferables
import pygame
from math import cos, sin, pi

print('Character_2D Starting')


class Player:
    def __init__(self, size): #, variant):
        self.__size = size
        # self.__variant = variant

        # Set Variables
        self.COLOR = '#C60018'
        self.SPEED_INCREASE_RATE = 2
        self.SPEED_DECREASE_RATE = 1
        self.SPEED_CAP = 4
        self.PUSH_DISTANCE = 3
        self.EFFECTIVE_MAX_SPEED = self.SPEED_CAP - self.SPEED_DECREASE_RATE

        self.attack_range = round(self.__size[0] * .8)
        self.attack_thickness = round(self.__size[0] * .8)


        self.laser_cooldown_default = 12
        self.laser_cooldown = 0

        # Dynamic variables
        self.speed = [0, 0]
        self.degrees = 0
        self.attack_direction = [0, -40]


        # Lists
        self.COLLIDER_RECT_LIST = []

        # player outline object, edges define where the collider objects will go

        self.png = pygame.image.load('venv/graphics/Teak/Push_1.png').convert_alpha()
        # self.png = pygame.image.load('graphics/Legacygraphics/custom/shell2.png').convert_alpha()
        # self.png = pygame.image.load('graphics/Helicopter/Helicopter.gif').convert_alpha()

        self.surf_default = pygame.transform.scale(self.png, (self.__size[0], self.__size[1]))
        self.surf = self.surf_default
        # self.surf.fill(self.COLOR)
        self.rect = self.surf.get_rect(center=(200, 200))

        # define collider sizes
        collider_longx = self.__size[0] * .9
        collider_shortx = self.__size[0] * .1

        collider_longy = self.__size[1] * .9
        collider_shorty = self.__size[1] * .1

        collider_zone = (self.__size[0]*2, self.__size[1]*2)

        # Create collider objects
        self.collider_top_surf = pygame.Surface((collider_longx, collider_shortx))
        self.collider_top_rect = self.collider_top_surf.get_rect(midtop=self.rect.midtop)

        self.collider_bottom_surf = pygame.Surface((collider_longx, collider_shortx))
        self.collider_bottom_rect = self.collider_bottom_surf.get_rect(midbottom=self.rect.midbottom)

        self.collider_left_surf = pygame.Surface((collider_shorty, collider_longy))
        self.collider_left_rect = self.collider_left_surf.get_rect(midleft=self.rect.midleft)

        self.collider_right_surf = pygame.Surface((collider_shorty, collider_longy))
        self.collider_right_rect = self.collider_right_surf.get_rect(midright=self.rect.midright)

        self.collider_zone_surf = pygame.Surface((collider_zone))
        self.collider_zone_rect = self.collider_zone_surf.get_rect(center=self.rect.center)

        # add colliders' rects to collider_rect_list
        self.COLLIDER_RECT_LIST.append(self.collider_top_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_bottom_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_left_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_right_rect)

    def movement(self, controls):
        # gathers all key presses
        keys = pygame.key.get_pressed()

        # use wasd
        if controls == 'WASD':
            up = keys[pygame.K_w]
            down = keys[pygame.K_s]
            left = keys[pygame.K_a]
            right = keys[pygame.K_d]
            del keys

        # or use arrow keys
        elif controls == 'ARROW':
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]
            del keys

        # otherwise no input detection
        else:
            up = False
            down = False
            left = False
            right = False
            del keys

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

            self.speed[0] = self.speed[0] + self.SPEED_INCREASE_RATE
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

            self.speed[1] = self.speed[1] + self.SPEED_INCREASE_RATE
            if self.speed[1] > self.SPEED_CAP:
                self.speed[1] = self.SPEED_CAP

        # diagonal input detection, doesn't impact speed just used to derive/store degrees
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

        if up and down and left and right:
            self.surf = self.surf_default
            self.degrees = 0

        # x axis speed decrease
        if self.speed[0] < 0:
            self.speed[0] = self.speed[0] + self.SPEED_DECREASE_RATE
        if self.speed[0] > 0:
            self.speed[0] -= self.SPEED_DECREASE_RATE
        if -self.SPEED_DECREASE_RATE+1 <= self.speed[0] <= self.SPEED_DECREASE_RATE-1:
            self.speed[0] = 0

        # y axis speed decrease
        if self.speed[1] < 0:
            self.speed[1] = self.speed[1] + self.SPEED_DECREASE_RATE
        if self.speed[1] > 0:
            self.speed[1] -= self.SPEED_DECREASE_RATE
        if -self.SPEED_DECREASE_RATE+1 <= self.speed[1] <= self.SPEED_DECREASE_RATE-1:
            self.speed[1] = 0

        # diagonal speed limiter
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
        self.rect.x = self.rect.x + self.speed[0]
        self.rect.y = self.rect.y + self.speed[1]

        # Place colliders in the proper place on player after they move
        self._moveColliders()

        # derive attack direction, could be done better with another function to use mouse or something
        if self.speed[0] or self.speed[1] != 0:
            self.attack_direction = [
                round(cos(self.degrees * pi / 180) * self.attack_range),
                round(sin(self.degrees * pi / 180) * self.attack_range)
            ]

    def movementMOUSE(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.centerx = mouse_pos[0]
        self.rect.centery = mouse_pos[1]

        self._moveColliders()

    def collision(self, box, box_list):
            # Top collision
            if self.collider_top_rect.bottom + 10 > box.rect.bottom:
                if self.collider_top_rect.colliderect(box.rect):
                    self.rect.top = box.rect.bottom
                    # self.speed[1] = 0
                    if box.type == 'box':
                        self._push(box, (0, -self.PUSH_DISTANCE),box_list)

            # Bottom collision
            if self.collider_bottom_rect.top - 10 < box.rect.top:
                if self.collider_bottom_rect.colliderect(box.rect):
                    self.rect.bottom = box.rect.top
                    # self.speed[1] = 0
                    if box.type == 'box':
                        self._push(box, (0, self.PUSH_DISTANCE),box_list)


            # Left collision
            if self.collider_left_rect.right + 10 > box.rect.right:
                if self.collider_left_rect.colliderect(box.rect):
                    self.rect.left = box.rect.right
                    if box.type == 'box':
                    # self.speed[0] = 0
                        self._push(box, (-self.PUSH_DISTANCE, 0),box_list)


            # Right collision
            if self.collider_right_rect.left - 10 < box.rect.left:
                if self.collider_right_rect.colliderect(box.rect):
                    self.rect.right = box.rect.left
                    # self.speed[0] = 0
                    if box.type == 'box':
                        self._push(box, (self.PUSH_DISTANCE, 0),box_list)

    def _moveColliders(self):
        self.collider_top_rect.midtop = self.rect.midtop
        self.collider_bottom_rect.midbottom = self.rect.midbottom
        self.collider_left_rect.midleft = self.rect.midleft
        self.collider_right_rect.midright = self.rect.midright
        self.collider_zone_rect.center = self.rect.center

    def _push(self, box, push_coord, box_list):
        box.rect.x = box.rect.x + push_coord[0]
        box.rect.y = box.rect.y + push_coord[1]

        if box_list[0].type == 'wall':
            pass
        else:
            for i in box_list:
                if box.rect.colliderect(i.collider_zone_rect):
                    if box.rect.center == i.rect.center:
                        # print('I I I'
                        pass
                    else:
                        # print('yeb')
                        box.collision(i, box_list)
                        box._moveColliders()


    def punch(self, configBufferList):
        x_surf = pygame.Surface((self.attack_range, self.attack_thickness))
        x_rect = x_surf.get_rect(center=[self.rect.centerx - self.attack_direction[1], self.rect.centery - self.attack_direction[0]])

        configBufferList.append(bufferables.animation([x_rect.centerx, x_rect.centery], self.attack_direction, "punch", (x_surf, x_rect)))

    def laser(self, configBufferList):
        if self.laser_cooldown == 0:

            x_surf = pygame.Surface((self.attack_range, self.attack_thickness))
            x_rect = x_surf.get_rect(center=[self.rect.centerx - self.attack_direction[1], self.rect.centery - self.attack_direction[0]])

            configBufferList.append(bufferables.animation([x_rect.centerx, x_rect.centery], self.attack_direction, "laser", (x_surf, x_rect)))
            self.laser_cooldown = self.laser_cooldown_default



    def cycle(self):
        if self.laser_cooldown > 0:
            self.laser_cooldown = self.laser_cooldown - 1


print('Character_2D Complete')
