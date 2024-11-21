import unittest

from src.utility.temperature import (
	kelvin_to_fahrenheit,
	fahrenheit_to_kelvin,
	centigrade_to_kelvin,
	kelvin_to_centigrade,
	fahrenheit_to_centigrade,
	centigrade_to_fahrenheit,
)

class TestTemperature(unittest.TestCase):

	def test__kelvin_to_fahrenheit__conversion(self):
		self.assertAlmostEqual(kelvin_to_fahrenheit(300), 80.33, places=2)

	def test__fahrenheit_to_kelvin__conversion(self):
		self.assertAlmostEqual(fahrenheit_to_kelvin(80.33), 300, places=2)

	def test__centigrade_to_kelvin__conversion(self):
		self.assertEqual(centigrade_to_kelvin(27), 300.15)

	def test__kelvin_to_centigrade__conversion(self):
		self.assertEqual(kelvin_to_centigrade(300.15), 27)

	def test__fahrenheit_to_centigrade__conversion(self):
		self.assertAlmostEqual(fahrenheit_to_centigrade(32), 0, places=2)

	def test__centigrade_to_fahrenheit__conversion(self):
		self.assertEqual(centigrade_to_fahrenheit(100), 212)

if __name__ == '__main__':
	unittest.main()
