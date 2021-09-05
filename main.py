import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PACMAN_SIZE = 48
FPS = 30

class Pacman:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def move_X(self, offset):

        if self.x + offset < 0 or self.x + offset > SCREEN_WIDTH - PACMAN_SIZE:
            return False
        self.x += offset
        return True

    def move_Y(self, offset):
        if self.y + offset < 0 or self.y + offset > SCREEN_HEIGHT - PACMAN_SIZE:
            return False
        self.y += offset
        return True
    
    def move(self):
        self.move_X(self.velocity_x)
        self.move_Y(self.velocity_y)

    def get_pos(self):
        return (self.x, self.y)

    def get_velocity(self):
        return (self.velocity_x, self.velocity_y)
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def update_directed_sprite(self):
        if self.velocity_y == 0:
            if self.velocity_x > 0: 
                self.directed_sprite = self.sprite
            else:
                self.directed_sprite = pygame.transform.rotate(self.sprite, 180)
        elif self.velocity_x == 0:
            if self.velocity_y > 0: 
                self.directed_sprite = pygame.transform.rotate(self.sprite, -90)
            else:
                self.directed_sprite = pygame.transform.rotate(self.sprite, 90)

    def set_velocity(self, v_x, v_y):
        self.velocity_x = v_x
        self.velocity_y = v_y
        self.update_directed_sprite()
    
    def get_sprite(self):
        return self.sprite

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.update_directed_sprite()

    def get_directed_sprite(self):
        return self.directed_sprite
   

def get_image(sheet, x, y, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image

pygame.init()
screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption('Pacman')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

pacman_spritesheet = pygame.image.load('pacman.png').convert_alpha()
pacman_sprite1 = get_image(pacman_spritesheet, 303, 709, 16, 16, 3)
pacman_sprite2 = get_image(pacman_spritesheet, 303, 692, 16, 16, 3)
sprite_order = 1
interval = 50
pacman = Pacman(pacman_sprite1, 0, 0)


#clock = pygame.time.Clock()
running = True
while running:
    #clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.set_velocity(-0.3, 0)
            if event.key == pygame.K_RIGHT:
                pacman.set_velocity(0.3, 0)
            if event.key == pygame.K_UP:
                pacman.set_velocity(0, -0.3)
            if event.key == pygame.K_DOWN:
                pacman.set_velocity(0, 0.3)
    pacman.move()
    interval -= 1
    if (interval == 0):
        interval = 50
        sprite_order = sprite_order % 2 + 1
    if (sprite_order == 1):
        pacman.set_sprite(pacman_sprite1)
    else:
        pacman.set_sprite(pacman_sprite2)
    screen.fill((0, 0, 0))
    screen.blit(pacman.get_directed_sprite(), pacman.get_pos())
    pygame.display.update()