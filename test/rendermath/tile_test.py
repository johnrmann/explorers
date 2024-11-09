import unittest

from src.rendermath.tile import (
	is_point_in_tile,
	tile_polygon,
)

class TestTileFunctions(unittest.TestCase):
	def test__is_point_in_tile(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertTrue(is_point_in_tile((0, 0), tile))
		self.assertTrue(is_point_in_tile((1, 1), tile))
		self.assertFalse(is_point_in_tile((3, 3), tile))
		self.assertFalse(is_point_in_tile((5, 5), tile))

if __name__ == '__main__':
	unittest.main()