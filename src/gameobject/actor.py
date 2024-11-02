from src.gameobject.gameobject import GameObject

class Actor(GameObject):
    _is_playable = True
    _is_played = True

    def __init__(self, pos=(0,0)):
        super()
        self.pos = pos
