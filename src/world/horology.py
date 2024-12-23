import math

from functools import lru_cache

EARTH_DAY_LENGTH = 24 * 60
EARTH_YEAR_LENGTH = 360

EARTH_TILT = 23.0

CONTRA_ARG_MSG = "Planetary tilt must be defined in rad xor deg"

def utc_date_tuple(utc: float, epoch = 0):
	"""Returns the (date, month, year) of the earth date."""
	days = (utc + epoch) // EARTH_DAY_LENGTH
	date = (days % 30) + 1
	month = ((days // 30) % 12) + 1
	year = (days // 30) // 12
	return (date, month, year)

def date_tuple_to_utc(date_tuple, epoch = 0) -> float:
	"""Converts (date, month, year) to UTC starting at optional epoch."""
	utc = 0
	date, month, year = date_tuple
	utc += ((date - 1) * EARTH_DAY_LENGTH)
	utc += ((month - 1) * EARTH_DAY_LENGTH * 30)
	utc += (year * EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)
	return utc - epoch

def utc_year_start(utc: float, epoch = 0) -> float:
	"""Gets the UTC timestamp of the start of the current year. Very nice for
	finding future holidays."""
	real_utc = utc + epoch
	non_year = real_utc % (EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)
	return utc - non_year

def utc_string(utc: float, epoch = 0) -> str:
	"""Converts game time to an earth date."""
	date, month, year = utc_date_tuple(utc, epoch)
	template = f"{year:04d}-{month:02d}-{date:02d}"
	return template.format(year=year, month=month, date=date)

def next_christmas(utc: float, epoch = 0) -> float:
	"""Finds the first christmas after landing."""
	date, month, year = utc_date_tuple(utc, epoch)
	if month == 12 and date > 25:
		return date_tuple_to_utc(
			(25, 12, year + 1),
			epoch=epoch,
		)
	else:
		return date_tuple_to_utc(
			(25, 12, year),
			epoch=epoch
		)

def moon_landing_anniv(landing_epoch: float):
	"""Calculates the X00th anniv of the moon landing. For convenience,
	returns the date and the anniv. number (2469-July-20, 500)."""
	_, _, year = utc_date_tuple(landing_epoch)
	century = (year // 100)
	decade_year = year % 100
	if decade_year >= 69:
		century += 1
	return (
		date_tuple_to_utc(
			(20, 8, (century * 100) + 69),
			landing_epoch
		),
		century - 19,
	)

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
