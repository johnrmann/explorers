import unittest

from src.world.horology import (
	Horology,
	utc_date_tuple,
	date_tuple_to_utc,
	utc_year_start,
	utc_string,
	next_christmas,
	moon_landing_anniv,
	EARTH_DAY_LENGTH,
	EARTH_YEAR_LENGTH
)

Y_1 = (EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)

Y_2500 = 2500 * (EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)
M_1 = 0
D_1 = 0

Y_1994 = 1994 * (EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)
M_3 = 2 * 30 * EARTH_DAY_LENGTH
D_27 = 26 * EARTH_DAY_LENGTH

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
	
	def test__utc_date_tuple(self):
		self.assertEqual(
			utc_date_tuple(Y_1994 + M_3 + D_27, 0),
			(27, 3, 1994),
		)
		self.assertEqual(
			utc_date_tuple(M_3 + D_27, Y_1994),
			(27, 3, 1994),
		)

	def test__utc_year_start(self):
		self.assertEqual(
			utc_year_start(Y_1994 + M_3 + D_27),
			Y_1994
		)
		self.assertEqual(
			utc_year_start(M_3 + D_27, epoch=Y_1994),
			0,
		)
		self.assertEqual(
			utc_year_start(0, epoch=M_3 + D_27),
			-(M_3 + D_27),
		)
		self.assertEqual(
			utc_year_start(Y_1 + 125, Y_2500),
			Y_1
		)
	
	def test__utc_string(self):
		self.assertEqual(
			utc_string(0),
			"0000-01-01",
		)
		self.assertEqual(
			utc_string(0, Y_2500),
			"2500-01-01",
		)
		self.assertEqual(
			utc_string(((11 * 30) * EARTH_DAY_LENGTH), Y_2500),
			"2500-12-01",
		)
		self.assertEqual(
			utc_string((((11 * 30) + 24) * EARTH_DAY_LENGTH), Y_2500),
			"2500-12-25",
		)

	def test__next_christmas(self):
		arrival = Y_2500 + M_3 + D_27
		next_xmas_utc = next_christmas(0, arrival)
		self.assertEqual(
			utc_string(next_xmas_utc, arrival),
			"2500-12-25",
		)

	def test__next_christmas__overflow(self):
		d_29 = 28 * EARTH_DAY_LENGTH
		m_12 = (11 * 30) * EARTH_DAY_LENGTH
		arrival = Y_2500 + m_12 + d_29
		next_xmas_utc = next_christmas(0, arrival)
		self.assertEqual(
			utc_string(next_xmas_utc, arrival),
			"2501-12-25",
		)

	def test__moon_landing_anniv__before(self):
		arrival = Y_2500
		moon_anniv_utc, x = moon_landing_anniv(arrival)
		self.assertEqual(
			utc_string(moon_anniv_utc, arrival),
			"2569-08-20"
		)
		self.assertEqual(x, 6)

	def test__moon_landing_anniv__overflow(self):
		arrival = Y_2500 + (70 * EARTH_DAY_LENGTH * EARTH_YEAR_LENGTH)
		moon_anniv_utc, x = moon_landing_anniv(arrival)
		self.assertEqual(
			utc_string(moon_anniv_utc, arrival),
			"2669-08-20"
		)
		self.assertEqual(x, 7)

if __name__ == "__main__":
	unittest.main()
