from staticentity import StaticEntity
from global_def import *

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
    
    def check_entity_collision(self, ent):
        if find_dist(self.get_pos(), ent.get_pos()) < MIN_COLLISION_DISTANCE:
            return True
        return False

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