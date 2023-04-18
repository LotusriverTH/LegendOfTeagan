import random
import pygame

screen_width, screen_height = 640, 480

def get_random_position():
    """return a random (x,y) position in the screen"""
    return (
        random.randint(0, screen_width - 1),  # randint includes both endpoints.
        random.randint(0, screen_height - 1),
    )

color_list = ["red", "orange", "yellow", "green", "cyan", "blue", "blueviolet"]
colors = [pygame.color.Color(c) for c in color_list]

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width, height = 64, 32
        self.color = random.choice(colors)
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # then move to a random position
        self.update()

    def update(self):
        # move to a random position
        self.rect.center = get_random_position()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprite Group Collision Demo")
    clock = pygame.time.Clock()  # for limiting FPS
    FPS = 6000
    exit_demo = False

    # create a sprite group to track the power ups.
    power_ups = pygame.sprite.Group()
    for _ in range(10):
        power_ups.add(PowerUp())  # create a new power up and add it to the group.

    # main loop
    while not exit_demo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_demo = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_demo = True
                elif event.key == pygame.K_SPACE:
                    power_ups.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                for _ in range(1000):
                    power_ups.add(PowerUp())

        # Update State: check for collisions
        for p in power_ups:
            if p.rect.collidepoint(pygame.mouse.get_pos()):
                power_ups.remove(p)
        # draw background
        screen.fill(pygame.Color("black"))  # use black background
        # draw sprites
        power_ups.draw(screen)
        # update screen
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()