from src.world.astronomy import Astronomy
from src.world.atmosphere import Atmosphere, AtmosphereElement
from src.world.horology import Horology, CENTURIA
from src.world.terrain import Terrain

class World:
	"""
	This class contains information about the "planetology" of the game world,
	including the terrain, horology (timekeeping), astronomy (distance from
	star, star brightness), and atmospheric composition.
	"""

	terrain: Terrain
	horology: Horology
	astronomy: Astronomy
	atmosphere: Atmosphere

	def __init__(
			self,
			terrain: Terrain,
			horology = None,
			astronomy = None,
			atmosphere_composition = None
	):
		if horology is None:
			horology = CENTURIA
		if astronomy is None:
			astronomy = Astronomy()
		if atmosphere_composition is None:
			atmosphere_composition = {
				key: 0 for key in AtmosphereElement
			}

		self.terrain = terrain
		self.horology = horology
		self.astronomy = astronomy
		self.atmosphere = Atmosphere(
			average=atmosphere_composition,
			astronomy=self.astronomy,
			planet_area=self.terrain.area
		)

	@property
	def dimensions(self):
		"""The dimensions of the world are defined by the terrain."""
		return self.terrain.dimensions

	def evolve(self, d_seconds=1):
		"""
		Evolves the world by `d_seconds` seconds.
		"""
		self.atmosphere.evolve(d_seconds)
