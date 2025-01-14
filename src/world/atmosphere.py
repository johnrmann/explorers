"""
This file contains functions and classes for a medium-complexity model of
planetary atmospheres.

Further Reading:
	- https://atmos.washington.edu/academics/classes/2001Q4/211/notes_greenhouse.html
"""

from enum import Enum

from src.mgmt.listener import Listener
from src.mgmt.event import Event
from src.mgmt.event_manager import EventManager
from src.mgmt.tick import Tickable

from src.utility.temperature import WATER_FREEZE_POINT
from src.utility.habitability import (
	temperature_habitability,
	pressure_habitability,
	HabitabilityFactor,
)

class AtmosphereElement(Enum):
	OXYGEN = 0
	NITROGEN = 1
	CARBON = 2
	METHANE = 3
	WATER = 4

ELEMENT_MOLAR_MASS = {
	AtmosphereElement.OXYGEN: 32,
	AtmosphereElement.NITROGEN: 28,
	AtmosphereElement.CARBON: 44,
	AtmosphereElement.METHANE: 16,
	AtmosphereElement.WATER: 18,
}

GREENHOUSE_WEIGHTS = {
	# Oxygen and Nitrogen are not proper greenhouse gasses, but still trap
	# heat in the atmosphere.
	AtmosphereElement.OXYGEN: 0.05,
	AtmosphereElement.NITROGEN: 0.02,
	# The other gasses do much more heat trapping.
	AtmosphereElement.CARBON: 0.50,
	AtmosphereElement.METHANE: 0.75,
	AtmosphereElement.WATER: 0.60,
}

EARTH_ATMOSPEHRE_AVG_COMPOSITION = {
	AtmosphereElement.OXYGEN: 210,
	AtmosphereElement.NITROGEN: 787,
	AtmosphereElement.CARBON: 1,
	AtmosphereElement.METHANE: 1,
	AtmosphereElement.WATER: 1,
}

EARTH_ATMOSPHERE_DENSITY = sum(
	ELEMENT_MOLAR_MASS[key] * count
	for key, count in EARTH_ATMOSPEHRE_AVG_COMPOSITION.items()
)

def make_atmosphere_composiiton(p_elements, n_density):
	"""
	Given a dict of the atmosphere elements and a density as a multiple of
	Earth's atmosphere, return the average composition of molar masses in
	that atmosphere.
	"""
	total = sum(p_elements.values())
	p_elements = {key: count / total for key, count in p_elements.items()}

	mass = sum(p * ELEMENT_MOLAR_MASS[key] for key, p in p_elements.items())
	mass_frac_earth = mass / EARTH_ATMOSPHERE_DENSITY

	avg = {}
	for key, count in p_elements.items():
		avg[key] = (count / mass_frac_earth) * n_density
	return avg

def greenhouseness(avg_composition):
	"""
	Returns how "greenhouse-y" a planet's atmosphere is. The higher the amount
	of greenhouse gasses, the more greenhouseness.
	"""
	return sum(
		count * GREENHOUSE_WEIGHTS[key]
		for key, count in avg_composition.items()
	)

EARTH_GREENHOUSE_WEIGHTS = greenhouseness(EARTH_ATMOSPEHRE_AVG_COMPOSITION)

# The officially accepted average surface temperature of Earth is ~59deg F
# (288 Kelvin), and the computed effective temperature is ~0deg F (255
# Kelvin). Earth's greenhouse factor must be the ratio between them.
ADJ_TPR = (288 / 255) - 1

def greenhouse_factor(weights):
	"""
	Returns the "greenhouse factor" - multiply this by the raw effective
	temperature to get the average surface temperature of a planet.
	"""
	k = ADJ_TPR * (greenhouseness(weights) / EARTH_GREENHOUSE_WEIGHTS)
	return 1 + k

# This is the Stefan-Boltzman constant in different units. The normal one,
# with a value of 5.67 * 10^-8, is in Watts per square meter per Kelvin^4.
# This one is based on multiples of Earth's solar radiation.
BOLTZMANN = (2.416 / 4) * 10**10

class Atmosphere(Listener, Tickable):
	"""
	The atmosphere of a planet is modeled by distributing many "units" of
	particles across the whole surface area of the planet. This will allow us
	to implement terraforming mechanics.

	For example, if the player plants a bunch of trees, the amount of carbon
	removed from the atmosphere will be proportional to the number of trees
	that the player planted.
	"""

	_evt_mgr = None

	total = None
	average = None
	composition = None

	delta = None
	transform: dict[
		tuple[AtmosphereElement, AtmosphereElement], tuple[int, int]
	] = None

	planet_area = 1024 * 512

	def __init__(
			self,
			total=None,
			average=None,
			astronomy=None,
			planet_area=(1024 * 512),
			evt_mgr: EventManager=None
	):
		self.total = {}
		self.average = {}
		self.composition = {}
		self.planet_area = planet_area
		self._evt_mgr = evt_mgr

		self.delta = {
			element: 0
			for element in AtmosphereElement
		}
		self.transform = {}

		if astronomy is not None:
			self.astronomy = astronomy
		else:
			raise ValueError('Astronomy is required')

		if total is None and average is None:
			raise ValueError('Please specify an atmospheric composition.')
		elif total is not None:
			self.total = total.copy()
			self.average = {
				key: count / self.planet_area
				for key, count in self.total.items()
			}
		elif average is not None:
			self.average = average.copy()
			self.total = {
				key: count * self.planet_area
				for key, count in self.average.items()
			}

		self._ensure_keys()
		self._recalculate_composition()
		if evt_mgr is not None:
			self._subscribe_to_events()


	def _ensure_keys(self):
		"""
		Ensures that all keys are in the atmosphere dictionaries.
		"""
		for key in AtmosphereElement:
			if key not in self.total:
				self.total[key] = 0
			if key not in self.average:
				self.average[key] = 0
			if key not in self.delta:
				self.delta[key] = 0


	def __str__(self):
		"""
		Prints a user-friendly atmosphere string to the console.
		"""
		tpr_kelvin = self.tpr_surface()
		tpr_far = (tpr_kelvin - 273.15) * 9/5 + 32
		s = "Atmosphere:\n"
		s += f"\tPressure: {self.density()}\n"
		s += f"\tTemperature: {tpr_kelvin} degK, {tpr_far} degF\n"
		s += "\tComposition:\n"
		for key, val in self.total.items():
			s += f"\t\t{key} - {val}\n"
		return s


	def _recalculate_composition(self):
		moles_total = self.moles_total()
		if moles_total == 0:
			self.composition = {
				key: 0
				for key in self.total.keys()
			}
		else:
			self.composition = {
				key: count / moles_total
				for key, count in self.total.items()
			}


	def _subscribe_to_events(self):
		self._evt_mgr.sub(AtmosphereChangeEvent, self)
		self._evt_mgr.sub(AtmosphereChangeDeltaEvent, self)
		self._evt_mgr.sub(AtmosphereChangeTransformEvent, self)


	@property
	def evt_mgr(self):
		"""
		The event manager for this atmosphere. Don't recommend reading,
		only writing (once).
		"""
		return self._evt_mgr


	@evt_mgr.setter
	def evt_mgr(self, value):
		if self._evt_mgr is not None:
			raise ValueError("Write-once property.")
		self._evt_mgr = value
		self._subscribe_to_events()


	def update(self, event):
		if isinstance(event, AtmosphereChangeEvent):
			for elem, count in event.delta.items():
				self.change_total(elem, count)
		elif isinstance(event, AtmosphereChangeDeltaEvent):
			for elem, count in event.delta.items():
				self.change_delta(elem, count)
		elif isinstance(event, AtmosphereChangeTransformEvent):
			for elems, amounts in event.transform.items():
				consumed_elem, produced_elem = elems
				consumed_amount, produced_amount = amounts
				self.change_transform(
					(consumed_elem, consumed_amount),
					(produced_elem, produced_amount)
				)


	def moles_total(self):
		"""
		Returns the total number of moles of stuff in the atmosphere.
		"""
		return sum(self.total.values())


	def moles_avg(self):
		"""
		Returns the number of moles found in the atmosphere per square.
		"""
		moles = 0
		for _, count in self.total.items():
			moles += count
		return moles / self.planet_area


	def total_molar_mass(self):
		"""
		Returns the total molecular mass of the atmosphere.
		"""
		total_molar_mass = 0
		for key, count in self.total.items():
			total_molar_mass += ELEMENT_MOLAR_MASS[key] * count
		return total_molar_mass


	def density(self):
		"""
		Returns the density of the atmosphere as a multiple of Earth's.
		"""
		raw = self.total_molar_mass() / self.planet_area
		return raw / EARTH_ATMOSPHERE_DENSITY


	def change_total(self, element, count):
		"""
		First derivative - change the amount of atmosphere element.
		"""
		self.total[element] += count
		self.average[element] = self.total[element] / self.planet_area
		self._recalculate_composition()


	def change_delta(self, element, count):
		"""
		Second derivative - change the amount the atmosphere is changing
		at.
		
		New(Atmosphere[element]) = Atmosphere[element] + count
		"""
		self.delta[element] += count


	def change_transform(self, consumed, produced):
		"""
		Another form of the second derivative - represents a chemical
		reaction that changes one element to another. Best used for situations
		like trees.
		"""
		consumed_elem, consumed_amount = consumed
		produced_elem, produced_amount = produced
		if consumed_amount * produced_amount < 0:
			raise ValueError("Values must have same sign.")
		pair = (consumed_elem, produced_elem)
		if pair not in self.transform:
			self.transform[pair] = (consumed_amount, produced_amount)
		else:
			old_consumed, old_produced = self.transform[pair]
			self.transform[pair] = (
				old_consumed + consumed_amount,
				old_produced + produced_amount
			)


	def tick_second(self, dt, utc):
		"""
		Mutates the atmosphere according to the delta.

		This is used for simulating terraforming over time. One instance would
		be the player planting trees, which would remove carbon from the
		atmosphere.

		Call this once per second (not frame!).
		"""
		for key, count in self.delta.items():
			self.total[key] += count * dt
			if self.total[key] < 0:
				self.total[key] = 0

		for elements, amounts in self.transform.items():
			consumed, produced = elements
			consumed_amount, produced_amount = amounts
			if consumed_amount == 0 and produced_amount == 0:
				continue
			ratio = produced_amount / consumed_amount
			to_consume = consumed_amount * dt
			to_produce = produced_amount * dt
			if to_consume > self.total[consumed]:
				to_consume = self.total[consumed]
				to_produce = to_consume * ratio
			self.total[consumed] -= to_consume
			self.total[produced] += to_produce

		self.average = {
			key: subtotal / self.planet_area
			for key, subtotal in self.total.items()
		}
		self._recalculate_composition()


	def albedo(self):
		"""
		The "albedo" of a planet is the fraction of sunlight that it reflects.
		Earth's albedo is 0.3, which means it reflects 30% of sunlight. There
		is not a direct relationship between atmospheric density and albedo,
		but there is a relationship, as thicker atmospheres can support more
		reflective particles (such as clouds).

		We therefore model albedo as a function of atmospheric density. We
		use the obesrved value of 0.22 for Mars as the minimum, and 0.9 as
		a maximum (for comparison, Venus is 0.75).

		TODO(jm) - add support for orbital mirrors and lenses.
		"""
		return max(0.22, min(0.9, self.density() - 0.70))


	def surface_energy(self):
		"""
		Returns the amount of energy that the planet's surface receives from
		the sun (accounting for energy reflected by the atmosphere).
		"""
		return self.astronomy.power_density * (1 - self.albedo())


	def tpr_effective(self):
		"""
		Returns the raw effective temperature of the planet.
		"""
		energy = self.surface_energy()
		tpr4 = energy * BOLTZMANN
		return pow(tpr4, 0.25)


	def tpr_surface(self):
		"""
		Retruns the average surface temperature of the planet.
		"""
		tpr_eff = self.tpr_effective()
		gh = greenhouse_factor(self.average)
		return tpr_eff * gh


	def tpr_daily_flux(self):
		"""
		Returns `n` where the planet's temperature varies between
		`self.tpr_surface() - n` and `self.tpr_surface() + n`.

		TODO(jm) - figure out a physics basis for this.
		"""
		return 10.0


	def tpr_latitude_flux(self):
		"""
		Returns `n` where the planet's temperature varies between
		`self.tpr_surface() - n` at the poles and `self.tpr_surface() + n`
		at the equator.
		"""
		return 15.0


	def delta_tpr_daily(self, time):
		"""
		Returns the temperature delta relative to the average temperature
		of the planet at the given time, where 0=noon and 0.5=midnight.
		"""
		if time > 0.5:
			return self.delta_tpr_daily(1 - time)
		time = 1 - (time * 4)
		return time * self.tpr_daily_flux()


	def delta_tpr_latitude(self, latitude):
		"""
		Returns the temperature at a given latitude where 0 is the equator and
		-1 is the south pole and 1 is the north pole.
		"""
		abs_lat = abs(latitude)
		dist_middle = (2 * abs_lat) - 1
		return -(dist_middle * self.tpr_latitude_flux())


	def tpr_at(self, time, latitude):
		"""
		Returns the temperature at a given time and latitude.
		"""
		delta_daily = self.delta_tpr_daily(time)
		delta_lat = self.delta_tpr_latitude(latitude)
		return self.tpr_surface() + delta_daily + delta_lat


	def is_frozen_at(self, latitude):
		"""
		Returns True if the planet is frozen at the given latitude at any time
		of the day (use noon as maximum). Useful for determining if water
		should become ice.
		"""
		return self.tpr_at(0.25, latitude) < WATER_FREEZE_POINT


	def habitability(self):
		"""
		Returns a dictionary of the habitability factors of the atmosphere.
		"""
		return {
			HabitabilityFactor.TEMPERATURE: temperature_habitability(
				self.tpr_surface()
			),
			HabitabilityFactor.PRESSURE: pressure_habitability(
				self.density()
			),
		}



class AtmosphereChangeEvent(Event):
	"""
	An event that signals a change in the atmosphere of a planet.
	"""

	delta: dict[AtmosphereElement, int]

	def __init__(self, delta):
		self.delta = delta

	def __eq__(self, other):
		return compare_atmosphere_dicts(self.delta, other.delta)

	def __str__(self):
		return f'AtmosphereChangeEvent({self.delta})'



class AtmosphereChangeDeltaEvent(Event):
	"""
	An event that signals a change in the rate of change of the atmosphere of
	a planet.
	"""

	delta: dict[AtmosphereElement, int]

	def __init__(self, delta):
		self.delta = delta

	def __eq__(self, other):
		return compare_atmosphere_dicts(self.delta, other.delta)

	def __str__(self):
		return f'AtmosphereChangeDeltaEvent({self.delta})'



class AtmosphereChangeTransformEvent(Event):
	"""
	An event that signals a change in the rate of atmospheric transformation
	of a planet.

	Atmospheric transformation is the process where something is changing
	one element to another, like a plant changing carbon dioxide to oxygen.
	Whereas atmospheric delta is the process of putting something or
	removing something from the atmosphere, like factories or carbon absorbers.
	"""

	transform: dict[tuple[AtmosphereElement, AtmosphereElement], tuple[int, int]]

	def __init__(self, transform):
		self.transform = transform

	def __eq__(self, other):
		return compare_atmosphere_dicts(self.transform, other.transform)

	def __str__(self):
		return f'AtmosphereChangeTransformEvent({self.transform})'


def compare_atmosphere_dicts(a, b):
	"""
	Compares two atmosphere dictionaries to see if they are "close enough".
	"""
	if a == b:
		return True
	a_keys = set(a.keys())
	b_keys = set(b.keys())
	if a_keys != b_keys:
		return False
	for key in a_keys:
		if a[key] != b[key]:
			return False
	return True
