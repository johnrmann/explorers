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

	minutes_in_day: int
	days_in_year: int
	tilt_deg: float

	def __init__(
		self,
		minutes_in_day = EARTH_DAY_LENGTH,
		days_in_year = EARTH_YEAR_LENGTH,
		tilt_deg = None,
		tilt_rad = None,
	):
		if tilt_deg is not None and tilt_rad is not None:
			raise AttributeError(CONTRA_ARG_MSG)
		elif tilt_rad is not None:
			self.tilt_deg = math.degrees(tilt_rad)
		elif tilt_deg is not None:
			self.tilt_deg = tilt_deg
		else:
			self.tilt_deg = EARTH_TILT
		self.minutes_in_day = minutes_in_day
		self.days_in_year = days_in_year
		# Computed properties.
		self.tilt_rad = math.radians(self.tilt_deg)
		self.minutes_in_year = self.minutes_in_day * self.days_in_year

	@lru_cache(maxsize=5)
	def utc_to_planet_calendar(self, utc: float):
		"""
		Converts UTC time to a date in the planet's calendar,
		as a (minute, day, year) tuple.
		"""
		minute = utc % self.minutes_in_day
		day = (utc // self.minutes_in_day) % self.days_in_year
		year = utc // self.minutes_in_year
		return (minute, day, year)

	@lru_cache(maxsize=5)
	def utc_to_planet_time_fracs(self, utc: float):
		"""
		Returns a tuple of fractions (0-0.999, 0-0.999) representing
		how far along we are in the (day, year). Very useful for sun
		angle calculations.
		"""
		minute, day, _ = self.utc_to_planet_calendar(utc)
		return (minute / self.minutes_in_day, day / self.days_in_year)
	
	def local_time_at_longitude(self, utc: float, longitude: float) -> float:
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

	def _brightness(self, local_time: float, f_year: float, lat: float):
		solar_noon_offset = 0.5 * math.sin(f_year * 2 * math.pi)
		solar_noon_offset *= math.sin(self.tilt_rad)
		solar_noon_offset *= lat

		adj_time = (local_time - solar_noon_offset) % 1.0
		day_night_factor = math.cos(adj_time * 2 * math.pi)
		seasonal_factor = math.cos(f_year * 2 * math.pi) * math.sin(self.tilt_rad) * lat

		return max(0, min(1, 0.5 + (0.5 * (day_night_factor + seasonal_factor))))

	def brightness(self, utc: float, lat_long):
		"""
		Calculates how bright it is at the given UTC and planet coordinates.
		"""
		lat, long = lat_long
		_, f_year = self.utc_to_planet_time_fracs(utc)
		local = self.local_time_at_longitude(utc, long)
		return self._brightness(local, f_year, lat)

CENTURIA = Horology(
	minutes_in_day=100,
	days_in_year=12,
	tilt_deg=0,
)
