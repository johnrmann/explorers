import unittest

from src.math.direction import Direction

from src.rendermath.multicell import (
	multicell_screen_top,
	multicell_screen_left,
	multicell_screen_right,
	multicell_screen_bottom,
	multicell_screen_diamond_cells,
	multicell_polygon_on_global_screen,
)

class MulticellTest(unittest.TestCase):
	def setUp(self):
		# Define a trivial case of a 1x1 square.
		self.trivial = ((1,1), (1,1))

		# Define a basic case of a perfect 2x2 square.
		p1 = (1,1)
		p2 = (2,2)
		self.basic = (p1, p2)

		# Oblong rects are trickier.
		q1 = (1,1)
		q2 = (4,2)
		self.oblong = (q1, q2)

	def test__multicell_screen__trivial(self):
		cos = [
			Direction.NORTHWEST,
			Direction.NORTHEAST,
			Direction.SOUTHEAST,
			Direction.SOUTHWEST
		]
		for co in cos:
			self.assertEqual(multicell_screen_top(self.trivial, co), (1,1))
			self.assertEqual(multicell_screen_left(self.trivial, co), (1,1))
			self.assertEqual(multicell_screen_right(self.trivial, co), (1,1))
			self.assertEqual(multicell_screen_bottom(self.trivial, co), (1,1))

	def test__multicell_screen_top__basic(self):
		self.assertEqual(multicell_screen_top(self.basic), (1,1))

	def test__multicell_screen_left__basic(self):
		self.assertEqual(multicell_screen_left(self.basic), (1,2))

	def test__multicell_screen_right__basic(self):
		self.assertEqual(multicell_screen_right(self.basic), (2,1))

	def test__multicell_screen_bottom__basic(self):
		self.assertEqual(multicell_screen_bottom(self.basic), (2,2))

	def test__multicell_screen_top__different_orientations(self):
		self.assertEqual(
			multicell_screen_top(self.basic, Direction.SOUTHEAST), (2,2)
		)
		self.assertEqual(
			multicell_screen_top(self.basic, Direction.NORTHEAST), (2,1)
		)
		self.assertEqual(
			multicell_screen_top(self.basic, Direction.SOUTHWEST), (1,2)
		)

	def test__mutlicell_screen_diamond_cells__oblong(self):
		top, right, bottom, left = multicell_screen_diamond_cells(self.oblong)
		self.assertEqual(top, (1,1))
		self.assertEqual(right, (4,1))
		self.assertEqual(bottom, (4,2))
		self.assertEqual(left, (1,2))

	def test__multicell_polygon_on_global_screen__trivial(self):
		tile_dims = (10, 10)
		expected_points = [(0, 5), (5, 10), (0, 15), (-5, 10)]
		points = list(
			multicell_polygon_on_global_screen(
				self.trivial, Direction.NORTHWEST, tile_dims
			)
		)
		self.assertEqual(points, expected_points)

	def test__multicell_polygon_on_global_screen__basic(self):
		tile_dims = (10, 10)
		expected_points = [(0, 5), (10, 15), (0, 25), (-10, 15)]
		points = list(
			multicell_polygon_on_global_screen(
				self.basic, Direction.NORTHWEST, tile_dims
			)
		)
		self.assertEqual(points, expected_points)

	def test__multicell_polygon_on_global_screen__oblong(self):
		tile_dims = (10, 10)
		expected_points = [(0, 5), (20, 25), (10, 35), (-10, 15)]
		points = list(
			multicell_polygon_on_global_screen(
				self.oblong, Direction.NORTHWEST, tile_dims
			)
		)
		self.assertEqual(points, expected_points)

	def test__multicell_polygon_on_global_screen__different_orientations(self):
		tile_dims = (10, 10)
		expected_points_se = [(0, -25), (10, -15), (0, -5), (-10, -15)]
		points_se = list(
			multicell_polygon_on_global_screen(
				self.basic, Direction.SOUTHEAST, tile_dims
			)
		)
		self.assertEqual(points_se, expected_points_se)

		expected_points_ne = [(15, -10), (25, 0), (15, 10), (5, 0)]
		points_ne = list(
			multicell_polygon_on_global_screen(
				self.basic, Direction.NORTHEAST, tile_dims
			)
		)
		self.assertEqual(points_ne, expected_points_ne)

		expected_points_sw = [(-15, -10), (-5, 0), (-15, 10), (-25, 0)]
		points_sw = list(
			multicell_polygon_on_global_screen(
				self.basic, Direction.SOUTHWEST, tile_dims
			)
		)
		self.assertEqual(points_sw, expected_points_sw)

if __name__ == '__main__':
	unittest.main()
