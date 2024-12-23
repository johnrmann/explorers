"""
Atmosphere generation.
"""

import random

from enum import Enum

from src.math.random import vary_value_percent

from src.world.astronomy import Astronomy
from src.world.atmosphere import (
	Atmosphere,
	AtmosphereElement,
	make_atmosphere_composiiton,
	EARTH_ATMOSPEHRE_AVG_COMPOSITION
)

class AtmosphereType(Enum):
	"""
	The type of atmosphere to create.

	Note that atmosphere type does not imply planet type. For example, it's
	possible to have a Mars-like atmosphere at an Earth-like orbit.

	See the docs for the _make functions for info about each type.
	"""
	EARTH_LIKE = 0
	MARS_LIKE = 1
	HOTHOUSE = 2
	TITAN_LIKE = 3
	PROTO_EARTH = 4

__BASE_PRESSURES = {
	AtmosphereType.EARTH_LIKE: 1,
	AtmosphereType.MARS_LIKE: 0.02,
	AtmosphereType.HOTHOUSE: 2,
	AtmosphereType.TITAN_LIKE: 1.5,
	AtmosphereType.PROTO_EARTH: 0.75,
}

__EARTH_VARIATION = {
	AtmosphereElement.OXYGEN: 0.03,
	AtmosphereElement.NITROGEN: 0.03,
	AtmosphereElement.CARBON: 0.01,
	AtmosphereElement.WATER: 0.01,
	AtmosphereElement.METHANE: 0.01,
}

__EARTH_RANGE = {
	key: (EARTH_ATMOSPEHRE_AVG_COMPOSITION[key], __EARTH_VARIATION[key])
	for key in AtmosphereElement
}

def _make_earth_like():
	"""
	Atmospheres of this type are very similar to Earth, with variations within
	a few percentage points.
	"""
	pressure = vary_value_percent(1.0, 0.1)
	p_composition = {
		key: vary_value_percent(value, variation)
		for key, (value, variation) in __EARTH_RANGE.items()
	}
	return make_atmosphere_composiiton(p_composition, pressure)

def _make_mars_like():
	"""
	Mars-like planets have a thin atmosphere entirely composed of carbon.
	"""
	pressure = random.uniform(0.01, 0.10)
	p_composition = {
		AtmosphereElement.CARBON: 1,
	}
	return make_atmosphere_composiiton(p_composition, pressure)

def _make_hothouse():
	"""
	Hothouse planets have a thick atmosphere composed entirely of carbon.
	"""
	base_pressure = __BASE_PRESSURES[AtmosphereType.HOTHOUSE]
	pressure = vary_value_percent(base_pressure, 0.25)
	p_composition = {
		AtmosphereElement.CARBON: 1,
	}
	return make_atmosphere_composiiton(p_composition, pressure)

def _make_titan_like():
	"""
	Titan-like atmospheres are thick and composed mostly of nitrogen and
	methane. They're pretty good candidates for terraforming.
	"""
	base_pressure = __BASE_PRESSURES[AtmosphereType.TITAN_LIKE]
	pressure = vary_value_percent(base_pressure, 0.25)
	p_composition = {
		AtmosphereElement.NITROGEN: vary_value_percent(0.95, 0.05),
		AtmosphereElement.METHANE: vary_value_percent(0.05, 0.05),
	}
	return make_atmosphere_composiiton(p_composition, pressure)

def _make_proto_earth():
	"""
	This is what Earth was like a few billion years ago.
	"""
	base_pressure = __BASE_PRESSURES[AtmosphereType.PROTO_EARTH]
	pressure = vary_value_percent(base_pressure, 0.40)
	p_composition = {
		AtmosphereElement.OXYGEN: vary_value_percent(0.005, 0.005),
		AtmosphereElement.NITROGEN: vary_value_percent(0.30, 0.05),
		AtmosphereElement.CARBON: vary_value_percent(0.70, 0.05),
	}
	return make_atmosphere_composiiton(p_composition, pressure)

def _generate_atmosphere_composition(atmosphere_type):
	"""
	Generates an atmosphere according to the given type.
	"""
	if atmosphere_type == AtmosphereType.EARTH_LIKE:
		return _make_earth_like()
	elif atmosphere_type == AtmosphereType.MARS_LIKE:
		return _make_mars_like()
	elif atmosphere_type == AtmosphereType.HOTHOUSE:
		return _make_hothouse()
	elif atmosphere_type == AtmosphereType.TITAN_LIKE:
		return _make_titan_like()
	elif atmosphere_type == AtmosphereType.PROTO_EARTH:
		return _make_proto_earth()
	else:
		raise ValueError(f'Unknown atmosphere type: {atmosphere_type}')

def generate_atmosphere(atmosphere_type, astronomy = None):
	"""
	Generates an atmosphere according to the given type.
	"""
	if astronomy is None:
		astronomy = Astronomy()
	comp = _generate_atmosphere_composition(atmosphere_type)
	return Atmosphere(
		planet_area = 1,
		average = comp,
		astronomy = astronomy,
	)
