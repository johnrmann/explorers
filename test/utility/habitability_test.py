import unittest

from src.utility.habitability import (
	# Tpr constants
	MIN_HABITABLE_TPR,
	MIN_OPTIMAL_TPR,
	MAX_OPTIMAL_TPR,
	MAX_HABITABLE_TPR,
	# Functions
	habitability_index,
	temperature_habitability,
	pressure_habitability,
	water_habitability
)

class HabitabilityTest(unittest.TestCase):
	def test__habitability_index__optimal(self):
		self.assertEqual(habitability_index(1, 1, 1), 1)

	def test__habitability_index__earth(self):
		earth_tpr_f = temperature_habitability(288.15)
		earth_pressure_f = pressure_habitability(1)
		earth_water_f = water_habitability(0.71)
		earth_breathability_f = 1
		self.assertAlmostEqual(
			habitability_index(earth_tpr_f, earth_pressure_f, earth_water_f),
			0.7245,
			3,
			earth_breathability_f
		)

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

if __name__ == '__main__':
	unittest.main()
