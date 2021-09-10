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