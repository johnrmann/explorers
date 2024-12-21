"""
Functions for calculating the habitability index of a planet, which is a
key factor in winning the game.
"""

import math

from enum import Enum

class HabitabilityFactor(Enum):
	"""
	Programmer-readable names for the factors that go into the habitability
	index.
	"""

	TOTAL = 0

	TEMPERATURE = 1
	PRESSURE = 2
	WATER = 3

def habitability_index(*factors):
	"""
	The habitability index is defined as PRODUCT(sqrt(factors)), where each
	factor is between zero and one.

	One factor of zero will (and should) make the whole index zero.	All factors
	being 1 will make the index 1. We use sqrt instead of a simple product
	because we don't want (0.5 * a bunch of ones) to be 0.5.
	"""
	roots = [math.sqrt(factor) for factor in factors]
	return math.prod(roots)

def _linear_habitability(min_hab, min_opt, max_opt, max_hab):
	def func(x):
		if min_hab <= x <= min_opt:
			lo_range = min_opt - min_hab
			return (x - min_hab) / lo_range
		elif min_opt <= x <= max_opt:
			return 1
		elif max_opt <= x <= max_hab:
			hi_range = max_hab - max_opt
			return 1 - ((x - max_opt) / hi_range)
		return 0
	return func

# These temperatures are equal to 74deg - 84deg F. The ideal climate for human
# habitation is somewhere between the Southern United States and the Caribbean.
# (Source: independent research by me)
MIN_OPTIMAL_TPR = 296.483
MAX_OPTIMAL_TPR = 302.039

# The minimum habitable temperature is the freezing point of water. Although
# humans can survive in colder temperatures, you can't have agriculture without
# liquid surface water.
MIN_HABITABLE_TPR = 273.15

# The maximum recorded temperature on Earth was 134deg F in Death Valley,
# California on 1913-July-10.
MAX_HABITABLE_TPR = 329.817

temperature_habitability = _linear_habitability(
	MIN_HABITABLE_TPR,
	MIN_OPTIMAL_TPR,
	MAX_OPTIMAL_TPR,
	MAX_HABITABLE_TPR
)

# The atmospheric pressure of the highest city in the world, La Paz, is 0.7atm.
# Use that minus some change as our min habitable pressure.
MIN_HABITABLE_PRESSURE = 0.6

# Use earth's atmosphere plus or minus change as optimum pressure.
MIN_OPTIMAL_PRESSURE = 0.9
MAX_OPTIMAL_PRESSURE = 1.1

# The water pressure at ten meters below sea level is 2atm, and scuba divers
# can dive at this depth for long periods w/o risking the bends.
MAX_HABITABLE_PRESSURE = 2.0

pressure_habitability = _linear_habitability(
	MIN_HABITABLE_PRESSURE,
	MIN_OPTIMAL_PRESSURE,
	MAX_OPTIMAL_PRESSURE,
	MAX_HABITABLE_PRESSURE
)

# All it takes is a little bit of water for the planet to be somewhat habitable.
MIN_HABITABLE_WATER = 0.1

# This is another case where Earth is _not_ the ideal. A 50/50 ratio of land to
# water maximizes agriculture.
MIN_OPTIMAL_WATER = 0.4
MAX_OPTIMAL_WATER = 0.6

# Too much water is better than too little. Put the maximum habitable water
# percentage beyond 1.
MAX_HABITABLE_WATER = 1.2

water_habitability = _linear_habitability(
	MIN_HABITABLE_WATER,
	MIN_OPTIMAL_WATER,
	MAX_OPTIMAL_WATER,
	MAX_HABITABLE_WATER
)
