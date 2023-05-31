import pygame

print('Boxes_2D Starting Legend of Teagan version')


class Box:
    def __init__(self, size, SPAWN_LOCATION, color):
        # Set Variables
        # test
        self.COLOR = color
        self.SPEED_INCREASE_RATE = 5
        self.SPEED_DECREASE_RATE = 2
        self.SPEED_CAP = 20
        self.__SPAWN_LOCATION = SPAWN_LOCATION
        self.PUSH_DISTANCE = 5
        self.DeleteFlag = False

        # Dynamic variables
        self.speed = [0, 0]
        self.__size = size  # (1)

        # Lists
        self.COLLIDER_RECT_LIST = []

        # box outline object, edges define where the collider objects will go
        self.surf = pygame.Surface((self.__size[0], self.__size[1]))
        self.surf.fill(self.COLOR)
        self.rect = self.surf.get_rect(center=(self.__SPAWN_LOCATION))

        # define collider sizes
        collider_longx = self.__size[0] * .9
        collider_shortx = self.__size[0] * .1

        collider_longy = self.__size[1] * .9
        collider_shorty = self.__size[1] * .1

        # Create collider objects
        self.collider_top_surf = pygame.Surface((collider_longx, collider_shorty))
        self.collider_top_rect = self.collider_top_surf.get_rect(midtop=self.rect.midtop)

        self.collider_bottom_surf = pygame.Surface((collider_longx, collider_shorty))
        self.collider_bottom_rect = self.collider_bottom_surf.get_rect(midbottom=self.rect.midbottom)

        self.collider_left_surf = pygame.Surface((collider_shortx, collider_longy))
        self.collider_left_rect = self.collider_left_surf.get_rect(midleft=self.rect.midleft)

        self.collider_right_surf = pygame.Surface((collider_shortx, collider_longy))
        self.collider_right_rect = self.collider_right_surf.get_rect(midright=self.rect.midright)

        # add colliders' rects to collider_rect_list
        self.COLLIDER_RECT_LIST.append(self.collider_top_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_bottom_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_left_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_right_rect)

    def collision(self, rect):
        # Top collision
        if self.collider_top_rect.bottom + 10 > rect.bottom:
            if self.collider_top_rect.colliderect(rect):
                self.rect.top = rect.bottom
                # self.speed[1] = 0
                self._push(rect, (0, -self.PUSH_DISTANCE))

        # Bottom collision
        if self.collider_bottom_rect.top - 10 < rect.top:
            if self.collider_bottom_rect.colliderect(rect):
                self.rect.bottom = rect.top
                # self.speed[1] = 0
                self._push(rect, (0, self.PUSH_DISTANCE))


        # Left collision
        if self.collider_left_rect.right + 10 > rect.right:
            if self.collider_left_rect.colliderect(rect):
                self.rect.left = rect.right
                # self.speed[0] = 0
                self._push(rect, (-self.PUSH_DISTANCE, 0))


        # Right collision
        if self.collider_right_rect.left - 10 < rect.left:
            if self.collider_right_rect.colliderect(rect):
                self.rect.right = rect.left
                # self.speed[0] = 0
                self._push(rect, (self.PUSH_DISTANCE, 0))

        self._moveColliders()

    def _push(self, rect, push_coord):
        rect.x += push_coord[0]
        rect.y += push_coord[1]
        # self.rect.x += push_coord[0]
        # self.rect.y += push_coord[1]

        self._moveColliders()


    def _moveColliders(self):
        self.collider_top_rect.midtop = self.rect.midtop
        self.collider_bottom_rect.midbottom = self.rect.midbottom
        self.collider_left_rect.midleft = self.rect.midleft
        self.collider_right_rect.midright = self.rect.midright

    def setDeleteFlag(self, do):
        if do:
            self.DeleteFlag = True


print('Boxes_2D Complete')
