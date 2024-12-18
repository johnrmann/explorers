import unittest
import pygame

from src.render.render_tile import (
	TileSurfaceCache,
	tile_screen_draw_position
)

class TestTileSurfaceCache(unittest.TestCase):

	def setUp(self):
		pygame.init()
		self.cache = TileSurfaceCache(zooms=[32, 64])

	def test__tile_surface_and_position__valid_input(self):
		surface, position = self.cache.tile_surface_and_position((100, 100), 32)
		self.assertIsInstance(surface, pygame.Surface)
		self.assertEqual(position, (84, 92))

class TestScreenDrawPositions(unittest.TestCase):

	def test__tile_screen_draw_position__valid_input(self):
		position = tile_screen_draw_position((100, 100), 32)
		self.assertEqual(position, (84, 92))

if __name__ == '__main__':
	unittest.main()
