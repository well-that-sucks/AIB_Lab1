from pacman import Pacman
from ghost import Ghost
from coin import Coin
from booster import Booster
from global_def import *

class Maze:
    def __init__(self, level_name):
        self.level = []
        self.level_name = level_name

    def load(self):
        with open('levels/' + str(self.level_name) + '.txt') as text:
            lines = text.readlines()
            self.level = [[c for c in line.strip()] for line in lines]

    def get_level(self):
        return self.level

    def get_level_name(self):
        return self.level_name

    def set_level(self, level_name):
        self.level_name = level_name
        self.load()

    def coord_to_block_position(self, pos):
        block_pos_x = pos[0] / SPRITE_SIZE
        block_pos_y = pos[1] / SPRITE_SIZE
        return (block_pos_x, block_pos_y)

    def check_collision(self, pos):
        block_pos = self.coord_to_block_position(pos)
        if (self.level[int(block_pos[1])][int(block_pos[0])] == '#'):
            return True
        return False

    def draw_level(self):
        i = 0
        for line in self.level:
            j = 0
            for block in line:
                if block == '#':
                    screen.blit(wall_sprite, (j * SPRITE_SIZE, i * SPRITE_SIZE))
                j += 1
            i += 1
    
    def init_entities(self):
        i = 0
        ghosts = []
        coins = []
        boosters = []
        sprite_index = 0
        for line in self.level:
            j = 0
            for block in line:
                if block == 'p':
                    pacman = Pacman(pacman_sprite1, j * SPRITE_SIZE, i * SPRITE_SIZE)
                if block == 'b':
                    ghosts.append(Ghost(ghost_sprites[sprite_index], j * SPRITE_SIZE, i * SPRITE_SIZE))
                    sprite_index += 1
                if block == 'c':
                    coins.append(Coin(coin_sprite, j * SPRITE_SIZE + SPRITE_SIZE / 3, i * SPRITE_SIZE + SPRITE_SIZE / 3, COIN_VALUE))
                if block == 'v':
                    coins.append(Coin(cherry_sprite, j * SPRITE_SIZE, i * SPRITE_SIZE, COIN_VALUE * 5))
                if block == 's':
                    coins.append(Coin(strawberry_sprite, j * SPRITE_SIZE, i * SPRITE_SIZE, COIN_VALUE * 5))
                if block == 'k':
                    boosters.append(Booster(booster_sprite, j * SPRITE_SIZE, i * SPRITE_SIZE))
                j += 1
            i += 1
        return pacman, ghosts, coins, boosters

    def check_block(self, block_x, block_y):
        return self.level[int(block_y)][int(block_x)]