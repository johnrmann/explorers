from src.world.horology import Horology, CENTURIA
from src.world.terrain import Terrain

class World:
	def __init__(self, terrain: Terrain, horology = CENTURIA):
		self.terrain = terrain
		self.horology = horology
	
	@property
	def dimensions(self):
		"""The dimensions of the world are defined by the terrain."""
		return self.terrain.dimensions
