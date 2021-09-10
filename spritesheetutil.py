import pygame

class SpriteSheetUtil:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load('resources/' + filename).convert_alpha()

    def get_image(self, x, y, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()  
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0))
        return image

    def load_spritesheet(self, filename):
        self.spritesheet = pygame.image.load('resources/' + filename).convert_alpha()
