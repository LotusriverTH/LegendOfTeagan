import pygame

print('Character_2D Starting')


class Player:
    def __init__(self, size):
        # Set Variables
        self.COLOR = '#C60018'
        self.SPEED_INCREASE_RATE = 8
        self.SPEED_DECREASE_RATE = 4
        self.SPEED_CAP = 16
        self.PUSH_DISTANCE = 5
        self.EFFECTIVE_MAX_SPEED = self.SPEED_CAP - self.SPEED_DECREASE_RATE

        # Dynamic variables
        self.speed = [0, 0]
        self.__size = size

        # Lists
        self.COLLIDER_RECT_LIST = []

        # player outline object, edges define where the collider objects will go
        self.surf = pygame.Surface((self.__size[0], self.__size[1]))
        self.surf.fill(self.COLOR)
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

        if controls == 'ARROW':
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]


        # Left movement
        if left:
            self.speed[0] -= self.SPEED_INCREASE_RATE
            if self.speed[0] < -self.SPEED_CAP:
                self.speed[0] = -self.SPEED_CAP
        # Right movement
        if right:
            self.speed[0] += self.SPEED_INCREASE_RATE
            if self.speed[0] > self.SPEED_CAP:
                self.speed[0] = self.SPEED_CAP
        # Up movement
        if up:
            self.speed[1] -= self.SPEED_INCREASE_RATE
            if self.speed[1] < -self.SPEED_CAP:
                self.speed[1] = -self.SPEED_CAP
        # Down movement
        if down:
            self.speed[1] += self.SPEED_INCREASE_RATE
            if self.speed[1] > self.SPEED_CAP:
                self.speed[1] = self.SPEED_CAP

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

    def _push(self, rect, push_coord):
        rect.x += push_coord[0]
        rect.y += push_coord[1]

    def _moveColliders(self):
        self.collider_top_rect.midtop = self.rect.midtop
        self.collider_bottom_rect.midbottom = self.rect.midbottom
        self.collider_left_rect.midleft = self.rect.midleft
        self.collider_right_rect.midright = self.rect.midright





print('Character_2D Complete')
