from staticentity import StaticEntity

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