import pygame
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SPRITE_SIZE = 48
BLOCK_AMOUNT_X = SCREEN_WIDTH / SPRITE_SIZE
BLOCK_AMOUNT_Y = SCREEN_HEIGHT / SPRITE_SIZE
ALLOWANCE_THRESHOLD = 0.3
COIN_VALUE = 10
MIN_COLLISION_DISTANCE = 20
FPS = 60

class StaticEntity:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
    
    def get_pos(self):
        return (self.x, self.y)

    def get_sprite(self):
        return self.sprite
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_sprite(self, sprite):
        self.sprite = sprite
        self.update_directed_sprite()
    
class MovingEntity(StaticEntity):
    pass

class Pacman(StaticEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def reset_pos(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def move_X(self, offset, maze):
        if self.x + offset < 0 or self.x + offset > SCREEN_WIDTH - SPRITE_SIZE or maze.check_collision((self.x + offset, self.y)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y)) or maze.check_collision((self.x + offset, self.y + SPRITE_SIZE - 1)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y + SPRITE_SIZE - 1)):     
            block_pos = maze.coord_to_block_position((self.x + offset, self.y))
            if abs(block_pos[1] - round(block_pos[1])) < ALLOWANCE_THRESHOLD and maze.check_block(block_pos[0] + offset / abs(offset), round(block_pos[1])) == '.':
                self.y = round(block_pos[1]) * SPRITE_SIZE
                return True
            return False
        self.x += offset
        return True

    def move_Y(self, offset, maze):
        if self.y + offset < 0 or self.y + offset > SCREEN_HEIGHT - SPRITE_SIZE or maze.check_collision((self.x, self.y + offset)) or maze.check_collision((self.x, self.y + offset + SPRITE_SIZE - 1)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset + SPRITE_SIZE - 1)):
            block_pos = maze.coord_to_block_position((self.x, self.y + offset))
            if abs(block_pos[0] - round(block_pos[0])) < ALLOWANCE_THRESHOLD and maze.check_block(round(block_pos[0]), block_pos[1] + offset / abs(offset)) == '.':
                self.x = round(block_pos[0]) * SPRITE_SIZE
                return True
            return False
        self.y += offset
        return True
    
    def move(self, maze):
        self.move_X(self.velocity_x, maze)
        self.move_Y(self.velocity_y, maze)

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

    def get_velocity(self):
        return (self.velocity_x, self.velocity_y)
    
    def get_directed_sprite(self):
        return self.directed_sprite

    def set_velocity(self, v_x, v_y):
        self.velocity_x = v_x
        self.velocity_y = v_y
        self.update_directed_sprite()

class Ghost(StaticEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.velocity_x = 0
        self.velocity_y = 0

    def reset_pos(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def move_X(self, offset, maze):
        if self.x + offset < 0 or self.x + offset > SCREEN_WIDTH - SPRITE_SIZE or maze.check_collision((self.x + offset, self.y)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y)) or maze.check_collision((self.x + offset, self.y + SPRITE_SIZE - 1)) or maze.check_collision((self.x + offset + SPRITE_SIZE - 1, self.y + SPRITE_SIZE - 1)):
            return False
        self.x += offset
        return True

    def move_Y(self, offset, maze):
        if self.y + offset < 0 or self.y + offset > SCREEN_HEIGHT - SPRITE_SIZE or maze.check_collision((self.x, self.y + offset)) or maze.check_collision((self.x, self.y + offset + SPRITE_SIZE - 1)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset)) or maze.check_collision((self.x + SPRITE_SIZE - 1, self.y + offset + SPRITE_SIZE - 1)):
            return False
        self.y += offset
        return True
    
    def move(self, maze):
        self.move_X(self.velocity_x, maze)
        self.move_Y(self.velocity_y, maze)

    def get_velocity(self):
        return (self.velocity_x, self.velocity_y)

    def set_velocity(self, v_x, v_y):
        self.velocity_x = v_x
        self.velocity_y = v_y

class Coin(StaticEntity):
    def __init__(self, sprite, x, y, value):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.value = value
        self.is_visible = True
    
    def change_visibility_state(self):
        self.is_visible = not(self.is_visible)

    def get_value(self):
        return self.value
    
    def get_visibility_state(self):
        return self.is_visible
    
    def set_value(self, new_value):
        self.value = new_value

class Maze:
    def __init__(self, level_name):
        self.level = []
        self.level_name = level_name

    def load(self):
        with open(str(self.level_name) + ".txt") as text:
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
                j += 1
            i += 1
        return pacman, ghosts, coins

    def check_block(self, block_x, block_y):
        return self.level[int(block_y)][int(block_x)]
            
            

def get_image(sheet, x, y, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()  
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image

def find_dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def check_entity_collision(ent1, ent2):
    if find_dist(ent1.get_pos(), ent2.get_pos()) < MIN_COLLISION_DISTANCE:
        return True
    return False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Pacman')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

maze = Maze('level1')
maze.load()

gameover_font = pygame.font.Font('freesansbold.ttf', 32)
score_font = pygame.font.Font('freesansbold.ttf', 24)

pacman_spritesheet = pygame.image.load('pacman.png').convert_alpha()

ghost_sprites = [get_image(pacman_spritesheet, 1, 83, 16, 16, 3),
    get_image(pacman_spritesheet, 601, 269, 16, 16, 3),
    get_image(pacman_spritesheet, 601, 641, 16, 16, 3),
    get_image(pacman_spritesheet, 401, 83, 16, 16, 3)]

wall_sprite = get_image(pacman_spritesheet, 86, 151, 16, 16, 3)
coin_sprite = get_image(pacman_spritesheet, 536, 586, 8, 8, 2)
pacman_sprite1 = get_image(pacman_spritesheet, 303, 709, 16, 16, 3)
pacman_sprite2 = get_image(pacman_spritesheet, 303, 692, 16, 16, 3)


running = True
clock = pygame.time.Clock()
reset = True

while running:
    if reset:
        pacman, ghosts, coins = maze.init_entities()
        score = 0
        sprite_order = 1
        interval = 5
        rand_helper = [-1, 1]
        is_lost = False
        reset = False

    while running and not(is_lost):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.set_velocity(-3, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.set_velocity(3, 0)
                if event.key == pygame.K_UP:
                    pacman.set_velocity(0, -3)
                if event.key == pygame.K_DOWN:
                    pacman.set_velocity(0, 3)

        pacman.move(maze)
        interval -= 1
        if (interval == 0):
            interval = 5
            sprite_order = sprite_order % 2 + 1
            for ghost in ghosts:
                new_velocity_x = (random.randint(0, 2) - 1) * 3
                if new_velocity_x == 0:
                    new_velocity_y = rand_helper[random.randint(0, 1)] * 3
                else:
                    new_velocity_y = 0
                ghost.set_velocity(new_velocity_x, new_velocity_y)
        if (sprite_order == 1):
            pacman.set_sprite(pacman_sprite1)
        else:
            pacman.set_sprite(pacman_sprite2)
        screen.fill((0, 0, 0))
        for ghost in ghosts:
            if check_entity_collision(pacman, ghost):
                is_lost = True
            ghost.move(maze)
            screen.blit(ghost.get_sprite(), ghost.get_pos())
        for coin in coins:
            if (coin.get_visibility_state()):
                if check_entity_collision(pacman, coin):
                    score += coin.get_value()
                    coin.change_visibility_state()
                else:
                    screen.blit(coin.get_sprite(), coin.get_pos())
        #print(score)
        screen.blit(pacman.get_directed_sprite(), pacman.get_pos())
        maze.draw_level()
        pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset = True
    if running and is_lost:
        screen.fill((0, 0, 0))
        gameover_ins = gameover_font.render('Game over!', True, (255, 255, 255))
        end_score_ins = gameover_font.render('Score: ' + str(score), True, (255, 255, 255))
        press_key_ins = gameover_font.render('Press SPACEBAR to restart the game', True, (255, 255, 255))
        screen.blit(gameover_ins, (SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 75))
        screen.blit(end_score_ins, (SCREEN_WIDTH / 2 - 58, SCREEN_HEIGHT / 2 - 38))
        screen.blit(press_key_ins, (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2))
        pygame.display.update()
