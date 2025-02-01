import unittest
import pygame

from src.render.tile_surface import (
	TileSurfaceCache,
	TileColors,
)



class TileColorsTest(unittest.TestCase):
	def test__init__requires_top(self):
		with self.assertRaises(ValueError):
			TileColors()


	def test__init__computes_left_right(self):
		colors = TileColors(top_color=(255, 0, 0))
		self.assertEqual(colors.left_color, (128, 0, 0))
		self.assertEqual(colors.right_color, (64, 0, 0))


	def test__init__custom_left_right(self):
		colors = TileColors(
			top_color=(255, 0, 0),
			left_color=(0, 255, 0),
			right_color=(0, 0, 255),
		)
		self.assertEqual(colors.left_color, (0, 255, 0))
		self.assertEqual(colors.right_color, (0, 0, 255))



class TestTileSurfaceCache(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.cache = TileSurfaceCache(zooms=[32, 64])


	def test__tile_surface_and_position__valid_input(self):
		surface = self.cache.tile_surface(32)
		self.assertIsInstance(surface, pygame.Surface)



if __name__ == '__main__':
	unittest.main()
