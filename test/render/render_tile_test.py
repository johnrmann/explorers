import unittest
import pygame

from src.render.render_tile import (
	TileSurfaceCache,
	tile_screen_draw_position,
	left_wall_screen_draw_position,
	right_wall_screen_draw_position
)

class TestTileSurfaceCache(unittest.TestCase):

	def setUp(self):
		pygame.init()
		self.cache = TileSurfaceCache(zooms=[32, 64])

	def test__tile_surface__valid_zoom(self):
		surface = self.cache.tile_surface(32)
		self.assertIsInstance(surface, pygame.Surface)

	def test__tile_surface__invalid_zoom(self):
		with self.assertRaises(KeyError):
			self.cache.tile_surface(128)

	def test__left_wall_surface__valid_zoom_height(self):
		surface = self.cache.left_wall_surface(32, 1)
		self.assertIsInstance(surface, pygame.Surface)

	def test__left_wall_surface__zero_height(self):
		surface = self.cache.left_wall_surface(32, 0)
		self.assertIsNone(surface)

	def test__right_wall_surface__valid_zoom_height(self):
		surface = self.cache.right_wall_surface(32, 1)
		self.assertIsInstance(surface, pygame.Surface)

	def test__right_wall_surface__zero_height(self):
		surface = self.cache.right_wall_surface(32, 0)
		self.assertIsNone(surface)

	def test__tile_surface_and_position__valid_input(self):
		surface, position = self.cache.tile_surface_and_position((100, 100), 32)
		self.assertIsInstance(surface, pygame.Surface)
		self.assertEqual(position, (84, 92))

	def test__left_wall_surface_and_position__valid_input(self):
		surf, pos = self.cache.left_wall_surface_and_position((100, 100), 32, 1)
		self.assertIsInstance(surf, pygame.Surface)
		self.assertEqual(pos, (84, 100))

	def test__right_wall_surface_and_position__valid_input(self):
		r_wall = self.cache.right_wall_surface_and_position((100, 100), 32, 1)
		surf, pos = r_wall
		self.assertIsInstance(surf, pygame.Surface)
		self.assertEqual(pos, (100, 100))

	def test__surfaces_and_positions__valid_input(self):
		surf_pos = self.cache.surfaces_and_positions((100, 100), 32, (1, 1))
		self.assertEqual(len(surf_pos), 3)
		self.assertIsInstance(surf_pos[0][0], pygame.Surface)
		self.assertEqual(surf_pos[0][1], (84, 92))
		self.assertIsInstance(surf_pos[1][0], pygame.Surface)
		self.assertEqual(surf_pos[1][1], (84, 100))
		self.assertIsInstance(surf_pos[2][0], pygame.Surface)
		self.assertEqual(surf_pos[2][1], (100, 100))

class TestScreenDrawPositions(unittest.TestCase):

	def test__tile_screen_draw_position__valid_input(self):
		position = tile_screen_draw_position((100, 100), 32)
		self.assertEqual(position, (84, 92))

	def test__left_wall_screen_draw_position__valid_input(self):
		position = left_wall_screen_draw_position((100, 100), 32)
		self.assertEqual(position, (84, 100))

	def test__right_wall_screen_draw_position__valid_input(self):
		position = right_wall_screen_draw_position((100, 100), 32)
		self.assertEqual(position, (100, 100))

if __name__ == '__main__':
	unittest.main()
