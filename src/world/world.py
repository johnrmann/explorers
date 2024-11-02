from src.world.horology import Horology
from src.world.terrain import Terrain

from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor

class World(object):
    def __init__(self, terrain: Terrain, horology = Horology()):
        self.utc = 0
        self.terrain = terrain
        self.horology = horology
        self.game_objects = []
    
    def new_player_character(self, pos):
        self.game_objects.append(Actor(pos=pos))