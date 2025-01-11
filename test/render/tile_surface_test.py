import unittest
import pygame

from src.render.tile_surface import (
	TileSurfaceCache,
)

class TestTileSurfaceCache(unittest.TestCase):

	def setUp(self):
		pygame.init()
		self.cache = TileSurfaceCache(zooms=[32, 64])

	def test__tile_surface_and_position__valid_input(self):
		surface = self.cache.tile_surface(32)
		self.assertIsInstance(surface, pygame.Surface)

if __name__ == '__main__':
	unittest.main()
