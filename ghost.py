from movingentity import MovingEntity

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