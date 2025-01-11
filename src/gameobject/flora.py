"""
This module contains everything related to flora (plants and trees).
"""

from src.gameobject.gameobject import GameObject
from src.mgmt.event import Event

from src.world.atmosphere import AtmosphereChangeTransformEvent, AtmosphereElement

# Use 0deg F - 120deg F as the default temperature range for flora.
DEFAULT_TPR_RANGE = (255, 322)

class FloraPrototype:
	"""
	We're going to have hundreds or possibly thousands of flora instances
	throughout the game world, and each of them will be one of a few dozen
	species. Therefore, we need to have a prototype for each species of flora
	that the game objects can reference, saving us memory.
	"""

	name: str

	max_health: float = 100

	# The amount of carbon that the flora can remove from the atmosphere.
	# Units: atmospheric units per second.
	carbon_sequestration: int = 0

	# The temperature range in which the flora can survive.
	# Degrees kelvin.
	min_tpr: float = -1
	max_tpr: float = -1

	# If we're outside the temperature range, this is how much health we lose
	# per second.
	# Units: health per kelvin per second.
	tpr_damage_rate: float = 0

	# If we're inside the temperature range, this is how much health we gain
	# per second.
	# Units: health per second.
	tpr_recovery_rate: float = 0

	def __init__(
			self,
			name = None,
			tpr_range=None,
			tpr_damage_rate=0, tpr_recovery_rate=0,
			carbon_sequestration=0,
			max_health=100,
	):
		if name is None:
			raise ValueError("Expected name!")
		if tpr_range is None:
			tpr_range = DEFAULT_TPR_RANGE
		self.min_tpr, self.max_tpr = tpr_range
		self.tpr_damage_rate = tpr_damage_rate
		self.tpr_recovery_rate = tpr_recovery_rate
		self.carbon_sequestration = carbon_sequestration
		self.max_health = max_health


	def tpr_health_delta(self, tpr):
		"""
		Input units: degrees kelvin.
		Output units: health per second.
		"""
		if tpr < self.min_tpr:
			delta = abs(tpr - self.min_tpr)
			return -delta * self.tpr_damage_rate
		elif self.min_tpr <= tpr <= self.max_tpr:
			return self.tpr_recovery_rate
		else:
			delta = abs(tpr - self.max_tpr)
			return -delta * self.tpr_damage_rate



PALM_TREE = FloraPrototype(name='Palm Tree', carbon_sequestration=0)

DEBUG_TREE = FloraPrototype(name='Debug Tree', carbon_sequestration=10_000)



class Flora(GameObject):
	"""
	Flora is good not only for decoration, but also for converting carbon into
	oxygen.
	"""

	health: float = 100
	prototype: FloraPrototype = None

	def __init__(
			self,
			prototype=None,
			**kwargs
	):
		super().__init__(size=(3,3,10), **kwargs)
		if prototype is None:
			raise ValueError("Expected prototype!")
		self.prototype = prototype
		self.health = prototype.max_health


	def image_path(self):
		return "assets/img/sprite/palm-tree.png"


	def _make_sequestration_event(self, direction = 1):
		"""
		Make an event that represents the sequestration of carbon. Use
		direction = -1 to undo the event.
		"""
		elems = (AtmosphereElement.CARBON, AtmosphereElement.OXYGEN)
		factor = self.prototype.carbon_sequestration
		amounts = (factor * direction, factor * direction)
		return AtmosphereChangeTransformEvent({
			elems: amounts
		})


	def on_init(self):
		self.evt_mgr.pub(self._make_sequestration_event(1))


	def on_remove(self):
		self.evt_mgr.pub(self._make_sequestration_event(-1))


	def tick(self, dt, utc):
		"""
		TODO(jm) - move this to tick_second in the future.
		"""
		tpr = self.game_mgr.world.atmosphere.tpr_effective()
		delta = self.prototype.tpr_health_delta(tpr) * dt
		self.health += delta
		self.health = min(self.prototype.max_health, max(0, self.health))
		if self.health <= 0:
			self.evt_mgr.pub(FloraDiedEvent(self))



class FloraDiedEvent(Event):
	"""
	An event to tell the game that a flora has died, and should be removed
	from the world.
	"""

	flora: Flora

	def __init__(self, flora):
		if not isinstance(flora, Flora):
			raise ValueError("Expected Flora!")
		super().__init__()
		self.flora = flora


	def __eq__(self, other):
		if not isinstance(other, FloraDiedEvent):
			return False
		return other.flora == self.flora
