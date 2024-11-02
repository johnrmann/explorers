EARTH_DAY_LENGTH = 24 * 60
EARTH_YEAR_LENGTH = 360

class Horology(object):
	"""
	Properites of time on the planet we're colonizing.

	For now, assume that a planet's day is shorter than its year,
	and that its year can be nicely divided into days.

	"UTC" refers to earth minutes (in-game seconds) since mission
	start, which just happens to be high noon on the spring
	equinox (easy for calculations!).
	"""

	minutes_in_day: int
	days_in_year: int

	def __init__(
		self,
		minutes_in_day = EARTH_DAY_LENGTH,
		days_in_year = EARTH_YEAR_LENGTH,
	):
		self.minutes_in_day = minutes_in_day
		self.days_in_year = days_in_year

	@property
	def minutes_in_year(self):
		return self.minutes_in_day * self.days_in_year

	def utc_to_planet_time_fracs(self, utc: int):
		"""
		Returns a tuple of fractions (0-0.999, 0-0.999) representing
		how far along we are in the (day, year). Very useful for sun
		angle calculations.
		"""
		minute, day, _ = self.utc_to_planet_calendar(utc)
		return (minute / self.minutes_in_day, day / self.days_in_year)

	def utc_to_planet_calendar(self, utc: int):
		"""
		Converts UTC time to a date in the planet's calendar,
		as a (minute, day, year) tuple.
		"""
		minute = utc % self.minutes_in_day
		day = (utc // self.minutes_in_day) % self.days_in_year
		year = utc // self.minutes_in_year
		return (minute, day, year)
	
	def local_time_at_longitude(self, utc: int, longitude: float) -> float:
		"""
		Returns a fraction between 0 and 0.99999... of the "local time"
		(temporal distance from high noon) at the given UTC and longitude
		(where longitude is a fraction, where 0 is on the prime meridian and
		+/-1 is on the international dateline).
		"""
		frac_day, _ = self.utc_to_planet_time_fracs(utc)
		adj_day = frac_day + (longitude / 2)
		if adj_day < 0:
			return 1 + adj_day
		return adj_day