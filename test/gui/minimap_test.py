import pygame

import unittest
from unittest.mock import Mock

from src.gui.minimap import minimap_image



class MinimapImageTest(unittest.TestCase):
	def test__minimap_image(self):
		terrain = Mock()
		terrain.dimensions = (10, 10)
		terrain.max_tile_height = 10
		terrain.min_tile_height = 0
		terrain.width = 10
		terrain.height = 10
		terrain.map = [[5 for _ in range(10)] for _ in range(10)]
		terrain.is_cell_ice = Mock(return_value=False)
		terrain.is_cell_water = Mock(return_value=False)

		surface = minimap_image(terrain, (10, 10))

		self.assertEqual(surface.get_width(), 10)
		self.assertEqual(surface.get_height(), 10)
		self.assertEqual(surface.get_at((0, 0)), (191, 0, 0))


	def test__minimap_image_ice(self):
		terrain = Mock()
		terrain.dimensions = (10, 10)
		terrain.max_tile_height = 10
		terrain.min_tile_height = 0
		terrain.width = 10
		terrain.height = 10
		terrain.map = [[5 for _ in range(10)] for _ in range(10)]
		terrain.is_cell_ice = Mock(return_value=True)
		terrain.is_cell_water = Mock(return_value=False)

		surface = minimap_image(terrain, (10, 10))

		self.assertEqual(surface.get_width(), 10)
		self.assertEqual(surface.get_height(), 10)
		self.assertEqual(surface.get_at((0, 0)), (250, 250, 250))


	def test__minimap_image_water(self):
		terrain = Mock()
		terrain.dimensions = (10, 10)
		terrain.max_tile_height = 10
		terrain.min_tile_height = 0
		terrain.width = 10
		terrain.height = 10
		terrain.map = [[5 for _ in range(10)] for _ in range(10)]
		terrain.is_cell_ice = Mock(return_value=False)
		terrain.is_cell_water = Mock(return_value=True)

		surface = minimap_image(terrain, (10, 10))

		self.assertEqual(surface.get_width(), 10)
		self.assertEqual(surface.get_height(), 10)
		self.assertEqual(surface.get_at((0, 0)), (0, 0, 200))



if __name__ == '__main__':
	unittest.main()
