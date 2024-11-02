from src.world.terrain import Terrain
from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor

class World(object):
    def __init__(self, terrain: Terrain):
        self.terrain = terrain
        self.game_objects = []
    
    def new_player_character(self, pos):
        self.game_objects.append(Actor(pos=pos))
