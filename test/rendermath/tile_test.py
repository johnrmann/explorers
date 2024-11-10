import unittest

from src.math.vector2 import Vector2
from src.rendermath.tile import (
	is_point_in_tile,
	tile_polygon,
	tile_top_y,
	tile_right_x,
	tile_bottom_y,
	tile_left_x,
	tile_width,
	tile_height,
	is_tile_in_screen,
	is_tile_in_rect,
)

class TestTileFunctions(unittest.TestCase):
	def test__is_point_in_tile(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertTrue(is_point_in_tile((0, 0), tile))
		self.assertTrue(is_point_in_tile((1, 1), tile))
		self.assertFalse(is_point_in_tile((3, 3), tile))
		self.assertFalse(is_point_in_tile((5, 5), tile))

	def test__tile_top_y(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_top_y(tile), -2)

	def test__tile_right_x(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_right_x(tile), 2)

	def test__tile_bottom_y(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_bottom_y(tile), 2)

	def test__tile_left_x(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_left_x(tile), -2)

	def test__tile_width(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_width(tile), 4)

	def test__tile_height(self):
		tile = tile_polygon((0, 0), (4, 4))
		self.assertEqual(tile_height(tile), 4)
	
	def test__is_tile_in_rect__center(self):
		tile = tile_polygon((0, 0), (4, 4))
		rect = (Vector2(-2, -2), Vector2(4, 4))
		self.assertTrue(is_tile_in_rect(tile, rect))

	def test__is_tile_in_rect__outside(self):
		tile = tile_polygon((0, 0), (4, 4))
		rect = (Vector2(5, 5), Vector2(4, 4))
		self.assertFalse(is_tile_in_rect(tile, rect))

	def test__is_tile_in_rect__on_edge(self):
		tile = tile_polygon((0, 0), (4, 4))
		rect = (Vector2(-2, -2), Vector2(2, 2))
		self.assertTrue(is_tile_in_rect(tile, rect))

	def test__is_tile_in__screen(self):
		tile = tile_polygon((0, 0), (4, 4))
		screen_dimensions = Vector2(10, 10)
		self.assertTrue(is_tile_in_screen(tile, screen_dimensions))

if __name__ == '__main__':
	unittest.main()