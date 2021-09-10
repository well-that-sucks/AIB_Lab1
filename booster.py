from staticentity import StaticEntity

class Booster(StaticEntity):
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.is_visible = True