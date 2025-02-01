"""
This file contains functions to debug code in the `src.world` package.
"""

from src.mgmt.event import Event

from src.world.atmosphere import (
	AtmosphereChangeEvent,
	AtmosphereElement,
	AtmosphereOverrideEvent
)


def interpret_atmosphere_command(words: list[str]) -> Event:
	"""
	Example commands:
		-	`atm.add_units oxygen 100`
		-	`atm.add_units oxygen 100 nitrogen 500`
		-	`atm.remove_units carbon 100`
		-	`atm.remove_units carbon 100 water 500`
	"""
	if words[0] == "atm.add_units":
		atmosphere = {}
		for i in range(1, len(words), 2):
			elem = AtmosphereElement.from_str(words[i])
			amount = int(words[i + 1])
			atmosphere[elem] = amount
		return AtmosphereChangeEvent(atmosphere)
	elif words[0] == "atm.remove_units":
		atmosphere = {}
		for i in range(1, len(words), 2):
			elem = AtmosphereElement.from_str(words[i])
			amount = int(words[i + 1])
			atmosphere[elem] = -amount
		return AtmosphereChangeEvent(atmosphere)
	elif words[0] == "atm.override":
		override_what = words[1]
		if override_what == "temperature":
			tpr = float(words[2])
			return AtmosphereOverrideEvent(
				property="temperature",
				value=tpr
			)
		elif override_what == "pressure":
			pressure = float(words[2])
			return AtmosphereOverrideEvent(
				property="pressure",
				value=pressure
			)
	elif words[0] == "atm.unoverride":
		unoverride_what = words[1]
		return AtmosphereOverrideEvent(
			property=unoverride_what,
			value=None,
			override=False
		)
	else:
		return None
