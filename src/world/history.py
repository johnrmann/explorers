from src.utility.habitability import HabitabilityFactor

class PlanetHistory:
	"""
	Represents the planet's history of habitability, atmospheric composition,
	temperature, etc.
	"""

	habitability = None

	def __init__(self, world):
		super().__init__()
		self.world = world
		self.habitability = {
			factor: [] for factor in HabitabilityFactor
		}

	def update(self, utc: float):
		"""
		Appends the current state to the history.
		"""
		habitability = self.world.habitability()
		for key, value in habitability.items():
			self.habitability[key].append((utc, value))
