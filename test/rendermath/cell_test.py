import unittest

from src.rendermath.cell import (
	cell_to_screen_transform,
	cell_position_on_global_screen,
	cell_polygon_on_global_screen,
	cell_origin_on_global_screen
)
from src.math.direction import Direction

class CellTest(unittest.TestCase):

	def test__cell_to_screen_transform__northwest(self):
		result = cell_to_screen_transform((1, 2), Direction.NORTHWEST)
		self.assertEqual(result, (-1, 3))


	def test__cell_to_screen_transform__northeast(self):
		result = cell_to_screen_transform((1, 2), Direction.NORTHEAST)
		self.assertEqual(result, (3, 1))


	def test__cell_to_screen_transform__southeast(self):
		result = cell_to_screen_transform((1, 2), Direction.SOUTHEAST)
		self.assertEqual(result, (1, -3))


	def test__cell_to_screen_transform__southwest(self):
		result = cell_to_screen_transform((1, 2), Direction.SOUTHWEST)
		self.assertEqual(result, (-3, -1))


	def test__cell_position_on_global_screen__origin(self):
		result = cell_position_on_global_screen(
			(0, 0), Direction.NORTHWEST, (64, 32)
		)
		self.assertEqual(result, (0, 0))


	def test__cell_position_on_global_screen__basic(self):
		result = cell_position_on_global_screen(
			(1, 2), Direction.NORTHWEST, (64, 32)
		)
		self.assertEqual(result, (-32, 48))


	def test__cell_position_on_global_screen__northeast(self):
		result = cell_position_on_global_screen(
			(1, 2), Direction.NORTHEAST, (64, 32)
		)
		self.assertEqual(result, (96, 16))


	def test__cell_position_on_global_screen__southeast(self):
		result = cell_position_on_global_screen(
			(1, 2), Direction.SOUTHEAST, (64, 32)
		)
		self.assertEqual(result, (32, -48))


	def test__cell_position_on_global_screen__southwest(self):
		result = cell_position_on_global_screen(
			(1, 2), Direction.SOUTHWEST, (64, 32)
		)
		self.assertEqual(result, (-96, -16))


	def test__cell_polygon_on_global_screen__origin(self):
		result = cell_polygon_on_global_screen(
			(0, 0), Direction.NORTHWEST, (64, 32)
		)
		self.assertEqual(result, [(0, -16), (32, 0), (0, 16), (-32, 0)])


	def test__cell_polygon_on_global_screen__basic(self):
		result = cell_polygon_on_global_screen(
			(1, 2), Direction.NORTHWEST, (64, 32)
		)
		self.assertEqual(
			result, [(-32, 32), (0, 48), (-32, 64), (-64, 48)]
		)


	def test__cell_polygon_on_global_screen__northeast(self):
		result = cell_polygon_on_global_screen(
			(1, 2), Direction.NORTHEAST, (64, 32)
		)
		self.assertEqual(
			result, [(96, 0), (128, 16), (96, 32), (64, 16)]
		)


	def test__cell_polygon_on_global_screen__southeast(self):
		result = cell_polygon_on_global_screen(
			(1, 2), Direction.SOUTHEAST, (64, 32)
		)
		self.assertEqual(
			result, [(32, -64), (64, -48), (32, -32), (0, -48)]
		)


	def test__cell_polygon_on_global_screen__southwest(self):
		result = cell_polygon_on_global_screen(
			(1, 2), Direction.SOUTHWEST, (64, 32)
		)
		self.assertEqual(
			result, [(-96, -32), (-64, -16), (-96, 0), (-128, -16)]
		)


	def test__cell_origin_on_global_screen__origin(self):
		result = cell_origin_on_global_screen(
			(0, 0), Direction.NORTHWEST, 64
		)
		self.assertEqual(result, (-32, -16))



if __name__ == '__main__':
	unittest.main()
