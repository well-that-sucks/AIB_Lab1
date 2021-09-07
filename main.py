import pygame
import random

from pygame.surfarray import blit_array

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SPRITE_SIZE = 48
SPRITE_CHANGE_INTERVAL = 5
BLINKING_BASE_INTERVAL = 20
BOT_CHANGE_DIRECTION_INTERVAL = 60
KILLER_MODE_DURATION = 600
ANIM_FRAME_DURATION = 10
RESPAWN_TIME = 300
ALLOWANCE_THRESHOLD = 0.35
BLINKING_WARNING_THRESHOLD = 200
EATEN_ENEMY_REWARD = 200
COIN_VALUE = 10
MIN_COLLISION_DISTANCE = 25
FPS = 60

class StaticEntity:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
        self.is_visible = True
    
    def change_visibility_state(self):
        self.is_visible = not(self.is_visible)

    def get_pos(self):
        return (self.x, self.y)

    def get_sprite(self):
        return self.sprite
    
    def get_visibility_state(self):
        return self.is_visible

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def set_sprite(self, sprite):
        self.sprite = sprite

class MovingEntity(StaticEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.directed_sprite = sprite
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_visible = True
    
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

class Ghost(MovingEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_visible = True
        self.invisibility_timer = 0
    
    def get_invisibility_timer(self):
        return self.invisibility_timer
    
    def set_invisibility_timer(self, timer):
        self.invisibility_timer = timer

class Coin(StaticEntity):
    def __init__(self, sprite, x, y, value):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.value = value
        self.is_visible = True

    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

class Booster(StaticEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.is_visible = True

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

levels = ['level1', 'level2', 'level3']
level_idx = 0
maze = Maze(levels[0])
maze.load()

transition_font = pygame.font.Font('freesansbold.ttf', 32)
hud_font = pygame.font.Font('freesansbold.ttf', 24)

pacman_spritesheet = pygame.image.load('pacman.png').convert_alpha()

ghost_sprites = [get_image(pacman_spritesheet, 1, 83, 16, 16, 3),
    get_image(pacman_spritesheet, 601, 269, 16, 16, 3),
    get_image(pacman_spritesheet, 601, 641, 16, 16, 3),
    get_image(pacman_spritesheet, 401, 83, 16, 16, 3)]

pacman_death_anim = [get_image(pacman_spritesheet, 201, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 218, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 235, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 252, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 269, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 286, 692, 16, 16, 3),
    get_image(pacman_spritesheet, 201, 709, 16, 16, 3),
    get_image(pacman_spritesheet, 218, 709, 16, 16, 3),
    get_image(pacman_spritesheet, 235, 709, 16, 16, 3),
    get_image(pacman_spritesheet, 252, 709, 16, 16, 3),
    get_image(pacman_spritesheet, 269, 709, 16, 16, 3),
    get_image(pacman_spritesheet, 286, 709, 16, 16, 3)]

ghost_killer_mode_sprite = get_image(pacman_spritesheet, 201, 168, 16, 16, 3)
blank_sprite = get_image(pacman_spritesheet, 286, 709, 16, 16, 3)
wall_sprite = get_image(pacman_spritesheet, 801, 604, 48, 48, 1)
coin_sprite = get_image(pacman_spritesheet, 536, 586, 8, 8, 2)
cherry_sprite = get_image(pacman_spritesheet, 601, 489, 16, 16, 3)
strawberry_sprite = get_image(pacman_spritesheet, 618, 489, 16, 16, 3)
booster_sprite = get_image(pacman_spritesheet, 669, 489, 16, 16, 3)
pacman_sprite1 = get_image(pacman_spritesheet, 303, 709, 16, 16, 3)
pacman_sprite2 = get_image(pacman_spritesheet, 303, 692, 16, 16, 3)


running = True
clock = pygame.time.Clock()
reset = True
lives = 3
score = 0

while running:
    if reset:
        maze.load()
        pacman, ghosts, coins, boosters = maze.init_entities()
        sprite_order = 1
        sprite_interval = SPRITE_CHANGE_INTERVAL
        bot_interval = BOT_CHANGE_DIRECTION_INTERVAL
        killer_timer = KILLER_MODE_DURATION
        blinking_interval = BLINKING_BASE_INTERVAL
        anim_interval = ANIM_FRAME_DURATION
        anim_ind = 0
        rand_helper = [-1, 1]
        is_killer_mode_active = False
        has_blinked = False
        is_anim_being_played = False
        has_player_lost = False
        are_all_coins_collected = False
        reset = False

    while running and not(has_player_lost) and not(are_all_coins_collected):
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

        if is_killer_mode_active:
            killer_timer -= 1
            if killer_timer < BLINKING_WARNING_THRESHOLD:
                blinking_interval -= 1
                if blinking_interval == 0: # Make it universal and independent from other values
                    blinking_interval = BLINKING_BASE_INTERVAL - (BLINKING_WARNING_THRESHOLD - killer_timer) // BLINKING_BASE_INTERVAL * 2
                    if blinking_interval < BLINKING_BASE_INTERVAL // 5:
                        blinking_interval = BLINKING_BASE_INTERVAL // 5
                    if has_blinked:
                        ind = 0
                        for ghost in ghosts:
                            ghost.set_sprite(ghost_killer_mode_sprite) # Fix code duplication
                            ind += 1
                    else:
                        for ghost in ghosts:
                            ghost.set_sprite(blank_sprite) # Fix code duplication
                    has_blinked = not(has_blinked)
            if killer_timer == 0:
                is_killer_mode_active = False
                ind = 0
                for ghost in ghosts:
                    ghost.set_sprite(ghost_sprites[ind]) # Fix code duplication
                    ind += 1

        sprite_interval -= 1
        if (sprite_interval == 0):
            sprite_interval = SPRITE_CHANGE_INTERVAL
            sprite_order = sprite_order % 2 + 1

        if (sprite_order == 1):
            pacman.set_sprite(pacman_sprite1)
        else:
            pacman.set_sprite(pacman_sprite2)

        screen.fill((0, 0, 0))

        are_all_coins_collected = True
        for coin in coins:
            if (coin.get_visibility_state()):
                if check_entity_collision(pacman, coin) and not(is_anim_being_played):
                    score += coin.get_value()
                    coin.change_visibility_state()
                else:
                    are_all_coins_collected = False
                    screen.blit(coin.get_sprite(), coin.get_pos())

        if are_all_coins_collected:
            level_idx += 1
            if (len(levels) > level_idx):
                maze.set_level(levels[level_idx])

        for booster in boosters:
            if (booster.get_visibility_state()):
                if check_entity_collision(pacman, booster) and not(is_anim_being_played):
                    is_killer_mode_active = True
                    killer_timer = KILLER_MODE_DURATION
                    blinking_interval = BLINKING_BASE_INTERVAL
                    for ghost in ghosts:
                        ghost.set_sprite(ghost_killer_mode_sprite)
                    booster.change_visibility_state()
                else:
                    screen.blit(booster.get_sprite(), booster.get_pos())

        if not(is_anim_being_played):
            pacman.move(maze)

        bot_interval -= 1
        for ghost in ghosts:
            if not(ghost.get_visibility_state()):
                ghost.set_invisibility_timer(ghost.get_invisibility_timer() - 1)
                if ghost.get_invisibility_timer() == 0:
                    ghost.change_visibility_state()
                    ghost.reset_pos()
            else:
                if bot_interval == 0:
                    new_velocity_x = (random.randint(0, 2) - 1) * 3
                    if new_velocity_x == 0:
                        new_velocity_y = rand_helper[random.randint(0, 1)] * 3
                    else:
                        new_velocity_y = 0
                    ghost.set_velocity(new_velocity_x, new_velocity_y)
                if check_entity_collision(pacman, ghost) and not(is_anim_being_played):
                    if is_killer_mode_active:
                       ghost.set_invisibility_timer(RESPAWN_TIME)
                       ghost.change_visibility_state()
                       score += EATEN_ENEMY_REWARD
                    else: 
                        anim_interval = ANIM_FRAME_DURATION
                        is_anim_being_played = True
                        anim_ind = 0
                if not(is_anim_being_played):
                    ghost.move(maze)
                screen.blit(ghost.get_sprite(), ghost.get_pos())
        if (bot_interval == 0):
            bot_interval = BOT_CHANGE_DIRECTION_INTERVAL

        if not(is_anim_being_played):
            screen.blit(pacman.get_directed_sprite(), pacman.get_pos())

        if (is_anim_being_played):
            anim_interval -= 1
            if anim_interval == 0:
                if anim_ind >= len(pacman_death_anim):
                    is_anim_being_played = False
                    lives -= 1
                    if lives == 0:
                        has_player_lost = True
                    else:
                        pacman.reset_pos()
                else:
                    anim_ind += 1
                    anim_interval = ANIM_FRAME_DURATION
            if anim_ind < len(pacman_death_anim):
                screen.blit(pacman_death_anim[anim_ind], pacman.get_pos())
        maze.draw_level()

        score_ins = hud_font.render('Score: ' + str(score), True, (255, 255, 255))
        lives_ins = hud_font.render('Lives: ' + str(lives), True, (255, 255, 255))
        level_ins = hud_font.render('Level: ' + str(level_idx + 1) + '/' + str(len(levels)), True, (255, 255, 255))
        screen.blit(score_ins, (0, 0))
        screen.blit(lives_ins, (0, 30))
        screen.blit(level_ins, (0, 60))

        pygame.display.update()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset = True
                    if has_player_lost:
                        maze.set_level(levels[0])
                        level_idx = 0
                        lives = 3
                        score = 0
                    if are_all_coins_collected and len(levels) <= level_idx:
                        running = False

    if running and has_player_lost:
        screen.fill((0, 0, 0))
        gameover_ins = transition_font.render('Game over!', True, (255, 255, 255))
        end_score_ins = transition_font.render('Score: ' + str(score), True, (255, 255, 255))
        press_key_ins = transition_font.render('Press SPACEBAR to restart the game', True, (255, 255, 255))
        screen.blit(gameover_ins, (SCREEN_WIDTH / 2 - 75, SCREEN_HEIGHT / 2 - 75))
        screen.blit(end_score_ins, (SCREEN_WIDTH / 2 - 58, SCREEN_HEIGHT / 2 - 38))
        screen.blit(press_key_ins, (SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2))
        pygame.display.update()

    if running and are_all_coins_collected:
        screen.fill((0, 0, 0))
        level_completed_ins = transition_font.render('You have completed the level!', True, (255, 255, 255))
        end_score_ins = transition_font.render('Score: ' + str(score), True, (255, 255, 255))
        offset_x = 350
        if (len(levels) > level_idx):
            press_key_ins = transition_font.render('Press SPACEBAR to procceed to the next level', True, (255, 255, 255))
        else:
            offset_x = 250
            press_key_ins = transition_font.render('Press SPACEBAR to close the game', True, (255, 255, 255))
        screen.blit(level_completed_ins, (SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 75))
        screen.blit(end_score_ins, (SCREEN_WIDTH / 2 - 58, SCREEN_HEIGHT / 2 - 38))
        screen.blit(press_key_ins, (SCREEN_WIDTH / 2 - offset_x, SCREEN_HEIGHT / 2))
        pygame.display.update()