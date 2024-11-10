import unittest

from src.rendermath.geometry import (
	sign,
	is_point_in_triangle,
	is_point_in_rect,
	is_point_in_screen
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

	def test__is_point_in_rect(self):
		rect = ((0, 0), (2, 2))
		self.assertTrue(is_point_in_rect((1, 1), rect))
		self.assertTrue(is_point_in_rect((0, 0), rect))
		self.assertFalse(is_point_in_rect((2, 2), rect))
		self.assertFalse(is_point_in_rect((3, 3), rect))

	def test__is_point_in_screen(self):
		dimensions = (2, 2)
		self.assertTrue(is_point_in_screen((1, 1), dimensions))
		self.assertTrue(is_point_in_screen((0, 0), dimensions))
		self.assertFalse(is_point_in_screen((2, 2), dimensions))
		self.assertFalse(is_point_in_screen((3, 3), dimensions))

if __name__ == '__main__':
	unittest.main()
