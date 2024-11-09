import unittest

from src.rendermath.geometry import (
	sign,
	is_point_in_triangle,
)

class GeometryTest(unittest.TestCase):
	def test__sign(self):
		self.assertEqual(sign((0, 0), (1, 1), (2, 2)), 0)
		self.assertEqual(sign((0, 0), (1, 0), (0, 1)), 1)
		self.assertEqual(sign((0, 0), (0, 1), (1, 0)), -1)

	def test__is_point_in_triangle(self):
		triangle = [(0, 0), (2, 0), (1, 2)]
		self.assertTrue(is_point_in_triangle((1, 1), triangle))
		self.assertTrue(is_point_in_triangle((1, 0), triangle))
		self.assertFalse(is_point_in_triangle((2, 2), triangle))
		self.assertFalse(is_point_in_triangle((3, 3), triangle))

if __name__ == '__main__':
	unittest.main()
