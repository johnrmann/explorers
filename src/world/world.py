from src.world.horology import Horology, CENTURIA
from src.world.terrain import Terrain
from src.world.world_stub import WorldStub

from src.gameobject.gameobject import GameObject
from src.gameobject.actor import Actor

class World(WorldStub):
	def __init__(self, terrain: Terrain, horology = CENTURIA):
		self.utc = 0.0
		self.terrain = terrain
		self.horology = horology
		self.game_objects = []
	
	@property
	def dimensions(self):
		"""The dimensions of the world are defined by the terrain."""
		return self.terrain.dimensions

	@property
	def player_character(self):
		"""Returns the currently selected player character."""
		for go in self.game_objects:
			if isinstance(go, Actor):
				if go._is_played: # TODO(jm) - evil private access
					return go
		raise ValueError("No player character - should never happen!")

	def new_player_character(self, pos):
		self.game_objects.append(Actor(pos=pos))
