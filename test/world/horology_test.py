import unittest

from src.world.horology import (
	Horology,
	utc_string,
	EARTH_DAY_LENGTH,
	EARTH_YEAR_LENGTH
)

EPOCH_YEAR_2500 = 2500 * (EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)

def earth_horology():
	return Horology()

def centuria_horology():
	"""
	The fictional planet of centuria has 100-minute days and 100-day
	years.
	"""
	return Horology(
		minutes_in_day=100,
		days_in_year=100
	)

earth = earth_horology()
centuria = centuria_horology()

class HorologyTest(unittest.TestCase):
	def test__minutes_in_year(self):
		self.assertEqual(earth.minutes_in_year, 24 * 60 * 12 * 30)
		self.assertEqual(centuria.minutes_in_year, 100 * 100)
	
	def test__utc_to_planet_calendar(self):
		self.assertEqual(
			earth.utc_to_planet_calendar(0),
			(0,0,0),
		)
		self.assertEqual(
			earth.utc_to_planet_calendar(42),
			(42,0,0),
		)

		two_yr = 2 * 12 * 30 * 24 * 60
		six_mo = 6 * 30 * 24 * 60
		twelve_hr = 12 * 60
		self.assertEqual(
			earth.utc_to_planet_calendar(two_yr + six_mo + twelve_hr),
			(twelve_hr, 6 * 30, 2)
		)

		one_cent_min = 1
		one_cent_day = 100
		one_cent_year = 100 * 100
		cent = one_cent_day + one_cent_min + one_cent_year
		self.assertEqual(
			centuria.utc_to_planet_calendar(cent),
			(1, 1, 1)
		)

	def test__utc_to_planet_time_fracs(self):
		self.assertEqual(
			earth.utc_to_planet_time_fracs(0),
			(0,0)
		)

		half_yr = 100 * 50
		three_yr = 3 * 100 * 100
		half_day = 50
		self.assertEqual(
			centuria.utc_to_planet_time_fracs(half_yr + half_day),
			(0.5, 0.5),
		)
		self.assertEqual(
			centuria.utc_to_planet_time_fracs(three_yr + half_yr + half_day),
			(0.5, 0.5)
		)
	
	def test__local_time_at_longitude(self):
		self.assertEqual(
			earth.local_time_at_longitude(0, 0),
			0.0
		)

		# If half a day passes after noon, it should be midnight.
		self.assertEqual(
			centuria.local_time_at_longitude(50, 0),
			0.5,
		)

		# If it's day at longitude 0, it should be night on the other side
		# of the planet.
		self.assertEqual(
			centuria.local_time_at_longitude(0, 1),
			0.5,
		)
		self.assertEqual(
			centuria.local_time_at_longitude(0, -1),
			0.5,
		)
	
	def test__utc_string(self):
		self.assertEqual(
			utc_string(0),
			"0000-01-01",
		)
		self.assertEqual(
			utc_string(0, EPOCH_YEAR_2500),
			"2500-01-01",
		)
		self.assertEqual(
			utc_string(((11 * 30) * EARTH_DAY_LENGTH), EPOCH_YEAR_2500),
			"2500-12-01",
		)
		self.assertEqual(
			utc_string((((11 * 30) + 24) * EARTH_DAY_LENGTH), EPOCH_YEAR_2500),
			"2500-12-25",
		)

if __name__ == "__main__":
	unittest.main()
