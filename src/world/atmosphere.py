"""
This file contains functions and classes for a medium-complexity model of
planetary atmospheres.

Further Reading:
	- https://atmos.washington.edu/academics/classes/2001Q4/211/notes_greenhouse.html
"""

import math

from enum import Enum

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

class Atmosphere:
	"""
	The atmosphere of a planet is modeled by distributing many "units" of
	particles across the whole surface area of the planet. This will allow us
	to implement terraforming mechanics.

	For example, if the player plants a bunch of trees, the amount of carbon
	removed from the atmosphere will be proportional to the number of trees
	that the player planted.
	"""

	total = None
	average = None
	composition = None

	delta = None

	planet_area = 1024 * 512

	def __init__(
			self,
			total=None,
			average=None,
			astronomy=None,
			planet_area=(1024 * 512)
	):
		self.total = {}
		self.average = {}
		self.composition = {}
		self.planet_area = planet_area

		self.delta = {
			element: 0
			for element in AtmosphereElement
		}

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

		self._recalculate_composition()

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

	def change_delta(self, element, count):
		"""
		Second derivative - change the amount the atmosphere is changing
		at.
		
		New(Atmosphere[element]) = Atmosphere[element] + count
		"""
		self.delta[element] += count

	def evolve(self, d_seconds=1):
		"""
		Mutates the atmosphere according to the delta.

		This is used for simulating terraforming over time. One instance would
		be the player planting trees, which would remove carbon from the
		atmosphere.

		Call this once per second (not frame!).
		"""
		for key, count in self.delta.items():
			self.total[key] += count * d_seconds
			if self.total[key] < 0:
				self.total[key] = 0
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
