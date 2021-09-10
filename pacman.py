import pygame
from movingentity import MovingEntity
from global_def import *

class Pacman(MovingEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def move_X(self, offset, maze):
        if self.x + offset < 0 or self.x + offset > SCREEN_WIDTH - SPRITE_SIZE or maze.check_collision((self.x + offset, self.y)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y)) or maze.check_collision((self.x + offset, self.y + SPRITE_SIZE - 1)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y + SPRITE_SIZE - 1)):     
            block_pos = maze.coord_to_block_position((self.x + offset, self.y))
            if offset != 0 and abs(block_pos[1] - round(block_pos[1])) < ALLOWANCE_THRESHOLD and maze.check_block(block_pos[0] + offset / abs(offset), round(block_pos[1])) != '#':
                self.y = round(block_pos[1]) * SPRITE_SIZE
                return True
            return False
        self.x += offset
        return True

    def move_Y(self, offset, maze):
        if self.y + offset < 0 or self.y + offset > SCREEN_HEIGHT - SPRITE_SIZE or maze.check_collision((self.x, self.y + offset)) or maze.check_collision((self.x, self.y + offset + SPRITE_SIZE - 1)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset + SPRITE_SIZE - 1)):
            block_pos = maze.coord_to_block_position((self.x, self.y + offset))
            if offset != 0 and abs(block_pos[0] - round(block_pos[0])) < ALLOWANCE_THRESHOLD and maze.check_block(round(block_pos[0]), block_pos[1] + offset / abs(offset)) != '#':
                self.x = round(block_pos[0]) * SPRITE_SIZE
                return True
            return False
        self.y += offset
        return True

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
        self.directed_sprite.set_colorkey((0, 0, 0)) 

    def get_directed_sprite(self):
        return self.directed_sprite

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.update_directed_sprite()