import unittest

from src.utility.calendar import (
	utc_float_to_utc_tuple,
	utc_float_to_mission_tuple,
	utc_float_to_utc_string,
	utc_float_to_mission_string,
	utc_tuple_to_utc_float,
	mision_tuple_to_utc_float,
	next_christmas,
	moon_landing_anniversary
)

class TestCalendar(unittest.TestCase):

	def test__utc_float_to_utc_tuple__correct_conversion(self):
		self.assertEqual(utc_float_to_utc_tuple(0), (1, 1, 1))
		self.assertEqual(utc_float_to_utc_tuple(1), (1, 1, 2))
		self.assertEqual(utc_float_to_utc_tuple(30), (1, 2, 1))
		self.assertEqual(utc_float_to_utc_tuple(360), (2, 1, 1))

	def test__utc_float_to_utc_tuple__with_epoch(self):
		epoch = 360 * (2469 - 1)
		july_20 = (6 * 30) + 19
		self.assertEqual(
			utc_float_to_utc_tuple(july_20, epoch=epoch),
			(2469, 7, 20)
		)

	def test__utc_float_to_mission_tuple__correct_conversion(self):
		self.assertEqual(utc_float_to_mission_tuple(0), (1, 1))
		self.assertEqual(utc_float_to_mission_tuple(360), (2, 1))
		self.assertEqual(utc_float_to_mission_tuple(30), (1, 31))

	def test__utc_float_to_utc_string__correct_format(self):
		self.assertEqual(utc_float_to_utc_string(0), "0001-01-01")
		self.assertEqual(utc_float_to_utc_string(360), "0002-01-01")
		self.assertEqual(utc_float_to_utc_string(30), "0001-02-01")

	def test__utc_float_to_utc_string__with_epoch(self):
		epoch = 360 * (2469 - 1)
		july_20 = (6 * 30) + 19
		self.assertEqual(
			utc_float_to_utc_string(0, epoch=epoch),
			"2469-01-01"
		)
		self.assertEqual(
			utc_float_to_utc_string(july_20, epoch=epoch),
			"2469-07-20"
		)

	def test__utc_float_to_mission_string__correct_format(self):
		self.assertEqual(utc_float_to_mission_string(0), "001-001")
		self.assertEqual(utc_float_to_mission_string(30), "031-001")
		self.assertEqual(utc_float_to_mission_string(360), "001-002")

	def test__utc_float_to_mission_string__with_days_per_year(self):
		self.assertEqual(
			utc_float_to_mission_string(0, days_per_year=100),
			"001-001"
		)
		self.assertEqual(
			utc_float_to_mission_string(1, days_per_year=100),
			"002-001"
		)
		self.assertEqual(
			utc_float_to_mission_string(101, days_per_year=100),
			"002-002"
		)

	def test__utc_tuple_to_utc_float__correct_conversion(self):
		self.assertEqual(utc_tuple_to_utc_float((1, 1, 1)), 0)
		self.assertEqual(utc_tuple_to_utc_float((2, 1, 1)), 360)
		self.assertEqual(utc_tuple_to_utc_float((1, 2, 1)), 30)

	def test__mision_tuple_to_utc_float__correct_conversion(self):
		self.assertEqual(mision_tuple_to_utc_float((1, 1)), 0)
		self.assertEqual(mision_tuple_to_utc_float((2, 1)), 360)
		self.assertEqual(mision_tuple_to_utc_float((1, 31)), 30)

	def test__next_christmas__correct_date(self):
		self.assertEqual(
			next_christmas(0),
			utc_tuple_to_utc_float((1, 12, 25))
		)

	def test__next_christmas__before_december(self):
		epoch = utc_tuple_to_utc_float((2350, 11, 1))
		self.assertEqual(
			next_christmas(
				utc_tuple_to_utc_float((2350, 11, 2), epoch=epoch),
				epoch=epoch
			),
			utc_tuple_to_utc_float((2350, 12, 25), epoch=epoch)
		)

	def test__next_christmas__after_december(self):
		epoch = utc_tuple_to_utc_float((2350, 12, 26))
		self.assertEqual(
			next_christmas(
				utc_tuple_to_utc_float((2350, 12, 27), epoch=epoch),
				epoch=epoch
			),
			utc_tuple_to_utc_float((2351, 12, 25), epoch=epoch)
		)

	def test__moon_landing_anniversary__before_year(self):
		epoch = utc_tuple_to_utc_float((1970, 1, 1))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2069)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 100)

	def test__moon_landing_anniversary__after_year(self):
		epoch = utc_tuple_to_utc_float((2065, 1, 1))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2069)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 100)

	def test__moon_landing_anniversary__after_july(self):
		epoch = utc_tuple_to_utc_float((2069, 8, 1))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2169)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 200)

	def test__moon_landing_anniversary__before_july(self):
		epoch = utc_tuple_to_utc_float((2069, 6, 1))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2069)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 100)

	def test__moon_landing_anniversary__in_july_before(self):
		epoch = utc_tuple_to_utc_float((2069, 7, 1))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2069)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 100)

	def test__moon_landing_anniversary__in_july_after(self):
		epoch = utc_tuple_to_utc_float((2069, 7, 21))
		utc, anniv = moon_landing_anniversary(0, epoch=epoch)
		year, month, day = utc_float_to_utc_tuple(utc, epoch=epoch)
		self.assertEqual(year, 2169)
		self.assertEqual(month, 7)
		self.assertEqual(day, 20)
		self.assertEqual(anniv, 200)

if __name__ == '__main__':
	unittest.main()
