import math

from functools import lru_cache

EARTH_YEAR_LENGTH = 360 * 1

class Horology(object):
	"""
	Properites of time on the planet we're colonizing.

	For now, assume that a planet's day is shorter than its year,
	and that its year can be nicely divided into days.

	"UTC" refers to earth minutes (in-game seconds) since mission
	start, which just happens to be high noon on the spring
	equinox (easy for calculations!).
	"""

	ticks_in_cycle = 0

	def __init__(self, ticks_in_cycle = EARTH_YEAR_LENGTH):
		self.ticks_in_cycle = ticks_in_cycle

	@lru_cache(maxsize=5)
	def utc_to_planet_calendar(self, utc: float):
		"""
		Converts UTC time to a date in the planet's calendar,
		as a (minute, day, year) tuple.
		"""
		tick = utc % self.ticks_in_cycle
		year = utc // self.ticks_in_cycle
		return (tick, year)

	def local_time_at_longitude(self, utc: float, longitude: float) -> float:
		"""
		Returns a fraction between 0 and 0.99999... of the "local time"
		(temporal distance from high noon) at the given UTC and longitude
		(where longitude is a fraction, where 0 is on the prime meridian and
		+/-1 is on the international dateline).
		"""
		frac_day = (utc % self.ticks_in_cycle) / self.ticks_in_cycle
		adj_day = frac_day + (longitude / 2)
		if adj_day < 0:
			return 1 + adj_day
		return adj_day

	def brightness(self, utc: float, long: float):
		"""
		Calculates how bright it is at the given UTC and planet coordinates.
		"""
		local = self.local_time_at_longitude(utc, long)
		if local <= 0.20 or local >= 0.80:
			return 7
		elif 0.70 <= local <= 0.80:
			d = (0.80 - local) / 0.10
			d *= 7
			return round(7 - d)
		elif 0.20 <= local <= 0.30:
			d = (0.30 - local) / 0.10
			d *= 7
			return round(d)
		return 0

CENTURIA = Horology(
	ticks_in_cycle=100,
)
