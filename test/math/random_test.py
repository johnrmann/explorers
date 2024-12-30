import unittest

from src.math.random import (
	vary_value_percent,
	vary_value_nominal,
	random_2d_integers_numpy
)

class TestRandomFunctions(unittest.TestCase):

	def test__vary_value_percent__within_range(self):
		value = 100
		p_variation = 0.1
		result = vary_value_percent(value, p_variation)
		self.assertTrue(90 <= result <= 110)

	def test__vary_value_nominal__within_range(self):
		value = 100
		variation = 100
		result = vary_value_nominal(value, variation)
		self.assertTrue(0 <= result <= 200)

	def test__random_2d_integers_numpy__errors_when_too_many_points(self):
		n = 100
		width = 4
		height = 8
		with self.assertRaises(ValueError):
			random_2d_integers_numpy(n, width, height)

	def test__random_2d_integers_numpy__returns_unique_points(self):
		n = 3
		width = 2
		height = 2
		for _ in range(20):
			points = random_2d_integers_numpy(n, width, height)
			points_set = set([tuple(point) for point in points])
			self.assertEqual(len(points), 3)
			self.assertEqual(len(points_set), 3)

if __name__ == '__main__':
	unittest.main()
