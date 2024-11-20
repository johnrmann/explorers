import math

class Astronomy:
	"""
	The Astronomy of a planet refers to its orbital characteristics, and the
	star it orbits.
	"""

	# Watts, fraction of Earth's sun
	star_luminosity = 1

	# AUs, fraction of Earth's orbital radius
	orbital_radius = 1

	def __init__(self, star_luminosity=1, orbital_radius=1):
		self.orbital_radius = orbital_radius
		self.star_luminosity = star_luminosity

	@property
	def power_density(self):
		"""
		Raw power that the planet gets from its star. Expressed as a fraction
		of Earth's.
		"""
		d2 = self.orbital_radius**2
		raw = self.star_luminosity / (d2 * 4 * math.pi)
		earth = 1 / (4 * math.pi)
		return raw / earth
