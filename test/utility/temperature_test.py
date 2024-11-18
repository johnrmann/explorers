import unittest

from src.utility.temperature import (
	temperature_habitability,
	kelvin_to_fahrenheit,
	fahrenheit_to_kelvin,
	centigrade_to_kelvin,
	kelvin_to_centigrade,
	fahrenheit_to_centigrade,
	centigrade_to_fahrenheit,
	MIN_HABITABLE_TPR,
	MIN_OPTIMAL_TPR,
	MAX_OPTIMAL_TPR,
	MAX_HABITABLE_TPR,
)

class TestTemperature(unittest.TestCase):

	def test__temperature_habitability__below_min_habitable(self):
		self.assertEqual(temperature_habitability(270), 0)

	def test__temperature_habitability__at_min_habitable(self):
		self.assertEqual(temperature_habitability(MIN_HABITABLE_TPR), 0)

	def test__temperature_habitability__at_optimal_cutoffs(self):
		self.assertEqual(temperature_habitability(MIN_OPTIMAL_TPR), 1)
		self.assertEqual(temperature_habitability(MAX_OPTIMAL_TPR), 1)

	def test__temperature_habitability__at_max_habitable(self):
		self.assertEqual(temperature_habitability(MAX_HABITABLE_TPR), 0)

	def test__temperature_habitability__above_max_habitable(self):
		self.assertEqual(temperature_habitability(330), 0)

	def test__temperature_habitability__within_optimal_range(self):
		self.assertEqual(temperature_habitability(300), 1)

	def test__temperature_habitability__below_optimal_range(self):
		# Note that the Earth surface temperature of 288K / 59F does not yield
		# an optimal score. This is because we want players to be able to do
		# better than Earth.
		self.assertAlmostEqual(temperature_habitability(288.15), 0.64286, 4)

	def test__temperature_habitability__above_optimal_range(self):
		self.assertAlmostEqual(temperature_habitability(310), 0.7134, 4)

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
