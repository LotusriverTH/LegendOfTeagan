import pygame

print('Boxes_2D Starting Legend of Teagan version')


class Box:
    def __init__(self, size, SPAWN_LOCATION, color):
        # Set Variables
        # test
        self.type = 'box'
        self.COLOR = color
        self.SPEED_INCREASE_RATE = 5
        self.SPEED_DECREASE_RATE = 2
        self.SPEED_CAP = 20
        self.__SPAWN_LOCATION = SPAWN_LOCATION
        self.PUSH_DISTANCE = 3
        self.DeleteFlag = False
        self.pushed = False

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

        collider_zone = (self.__size[0]*2, self.__size[1]*2)


        # Create collider objects
        self.collider_top_surf = pygame.Surface((collider_longx, collider_shorty))
        self.collider_top_rect = self.collider_top_surf.get_rect(midtop=self.rect.midtop)

        self.collider_bottom_surf = pygame.Surface((collider_longx, collider_shorty))
        self.collider_bottom_rect = self.collider_bottom_surf.get_rect(midbottom=self.rect.midbottom)

        self.collider_left_surf = pygame.Surface((collider_shortx, collider_longy))
        self.collider_left_rect = self.collider_left_surf.get_rect(midleft=self.rect.midleft)

        self.collider_right_surf = pygame.Surface((collider_shortx, collider_longy))
        self.collider_right_rect = self.collider_right_surf.get_rect(midright=self.rect.midright)

        # OLD VERSION OVERWRITE DEBUG`
        # self.collider_top_surf = pygame.Surface((collider_longx, collider_shortx))
        # self.collider_top_rect = self.collider_top_surf.get_rect(midtop=self.rect.midtop)
        #
        # self.collider_bottom_surf = pygame.Surface((collider_longx, collider_shortx))
        # self.collider_bottom_rect = self.collider_bottom_surf.get_rect(midbottom=self.rect.midbottom)
        #
        # self.collider_left_surf = pygame.Surface((collider_shorty, collider_longy))
        # self.collider_left_rect = self.collider_left_surf.get_rect(midleft=self.rect.midleft)
        #
        # self.collider_right_surf = pygame.Surface((collider_shorty, collider_longy))
        # self.collider_right_rect = self.collider_right_surf.get_rect(midright=self.rect.midright)
        #
        self.collider_zone_surf = pygame.Surface(collider_zone)
        self.collider_zone_rect = self.collider_zone_surf.get_rect(center=self.rect.center)


        # add colliders' rects to collider_rect_list
        self.COLLIDER_RECT_LIST.append(self.collider_top_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_bottom_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_left_rect)
        self.COLLIDER_RECT_LIST.append(self.collider_right_rect)

    def collision(self, box, box_list):
        # Top collision
        if self.collider_top_rect.bottom + 10 > box.rect.bottom:
            if self.collider_top_rect.colliderect(box.rect):
                self.rect.top = box.rect.bottom
                # self.speed[1] = 0
                if box.type == 'box':
                    self._push(box, (0, -self.PUSH_DISTANCE), box_list)

        # Bottom collision
        if self.collider_bottom_rect.top - 10 < box.rect.top:
            if self.collider_bottom_rect.colliderect(box.rect):
                self.rect.bottom = box.rect.top
                # self.speed[1] = 0
                if box.type == 'box':
                    self._push(box, (0, self.PUSH_DISTANCE), box_list)


        # Left collision
        if self.collider_left_rect.right + 10 > box.rect.right:
            if self.collider_left_rect.colliderect(box.rect):
                self.rect.left = box.rect.right
                # self.speed[0] = 0
                if box.type == 'box':
                    self._push(box, (-self.PUSH_DISTANCE, 0), box_list)


        # Right collision
        if self.collider_right_rect.left - 10 < box.rect.left:
            if self.collider_right_rect.colliderect(box.rect):
                self.rect.right = box.rect.left
                # self.speed[0] = 0
                if box.type == 'box':
                    self._push(box, (self.PUSH_DISTANCE, 0), box_list)

        self._moveColliders()


    def _push(self, box, push_coord, box_list):
        box.rect.x = box.rect.x + push_coord[0]
        box.rect.y = box.rect.y + push_coord[1]
        box.pushed = True

        for i in box_list:
            if box.rect.colliderect(i.collider_zone_rect):
                if True:
                    # print('True')
                    if box.rect.center == i.rect.center:
                        # print('I???')
                        pass
                    else:
                        # print('yeb???')
                        try:
                            box.collision(i, box_list)
                            box._moveColliders()
                        except RecursionError as err:
                            print('Sorry but this maze solver was not able to finish '
                                  'analyzing the maze: {}'.format(err.args[0]))
                            box.setDeleteFlag(True)
                            continue


    def _moveColliders(self):

        self.collider_top_rect.midtop = self.rect.midtop
        self.collider_bottom_rect.midbottom = self.rect.midbottom
        self.collider_left_rect.midleft = self.rect.midleft
        self.collider_right_rect.midright = self.rect.midright
        self.collider_zone_rect.center = self.rect.center
        self.pushed = False

    def setDeleteFlag(self, do):
        if do:
            self.DeleteFlag = True


print('Boxes_2D Complete')
