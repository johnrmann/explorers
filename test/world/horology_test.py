import unittest

from src.world.horology import (
	Horology,
	EARTH_YEAR_LENGTH
)

def earth_horology():
	return Horology()

def centuria_horology():
	"""
	The fictional planet of centuria has 100-minute days and 100-day
	years.
	"""
	return Horology(
		ticks_in_cycle=100,
	)

earth = earth_horology()
centuria = centuria_horology()

class HorologyTest(unittest.TestCase):
	def test__utc_to_planet_calendar(self):
		self.assertEqual(
			earth.utc_to_planet_calendar(0),
			(0,0),
		)
		self.assertEqual(
			earth.utc_to_planet_calendar(42),
			(42,0),
		)

		two_yr = 2 * 12 * 30
		six_mo = 6 * 30
		self.assertEqual(
			earth.utc_to_planet_calendar(two_yr + six_mo),
			(six_mo, 2)
		)

		one_cent_min = 1
		one_cent_year = 100
		cent = one_cent_min + one_cent_year
		self.assertEqual(
			centuria.utc_to_planet_calendar(cent),
			(1, 1)
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

if __name__ == "__main__":
	unittest.main()
