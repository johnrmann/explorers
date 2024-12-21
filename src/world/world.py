from src.world.astronomy import Astronomy
from src.world.atmosphere import Atmosphere, AtmosphereElement
from src.world.history import PlanetHistory
from src.world.horology import Horology, CENTURIA
from src.world.terrain import Terrain

from src.utility.habitability import HabitabilityFactor, habitability_index

class World:
	"""
	This class contains information about the "planetology" of the game world,
	including the terrain, horology (timekeeping), astronomy (distance from
	star, star brightness), and atmospheric composition.
	"""

	game_mgr = None

	terrain: Terrain
	horology: Horology
	astronomy: Astronomy
	atmosphere: Atmosphere

	history: PlanetHistory

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

		self.history = PlanetHistory(self)

	@property
	def dimensions(self):
		"""The dimensions of the world are defined by the terrain."""
		return self.terrain.dimensions

	def evolve(self, d_seconds=1):
		"""
		Evolves the world by `d_seconds` seconds.
		"""
		self.atmosphere.evolve(d_seconds)
		self.history.update(self.game_mgr.utc)

	def habitability(self):
		"""
		Returns a dictionary of the habitability factors of the atmosphere.
		"""
		atm_hab = self.atmosphere.habitability()
		hab = atm_hab.copy()
		hab[HabitabilityFactor.TOTAL] = habitability_index(*hab.values())
		return hab
