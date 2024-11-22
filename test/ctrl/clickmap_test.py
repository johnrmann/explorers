import unittest
import pygame

from src.ctrl.clickmap import ClickMap

class TestClickMap(unittest.TestCase):

	def setUp(self):
		pygame.init()
		self.screen_dimensions = (32, 32)
		self.clickmap = ClickMap(self.screen_dimensions)

	def tearDown(self):
		pygame.quit()

	def test__init__raises_ValueError(self):
		with self.assertRaises(ValueError):
			ClickMap()

	def test__init__sets_screen_dimensions(self):
		self.assertEqual(
			self.clickmap.screen_dimensions,
			self.screen_dimensions
		)

	def test__is_terrain__returns_true_for_terrain_pixel(self):
		alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask.fill((0, 0, 0, 255))
		self.clickmap.mark_terrain((0, 0), alpha_mask)
		self.assertTrue(self.clickmap.is_terrain((0, 0)))

	def test__is_terrain__returns_false_for_game_object_pixel(self):
		alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask.fill((255, 255, 255, 255))
		self.clickmap.mark_game_object('obj1', (0, 0), alpha_mask)
		self.assertFalse(self.clickmap.is_terrain((0, 0)))

	def test__game_object_at__returns_none_if_no_game_object(self):
		self.assertIsNone(self.clickmap.game_object_at((0, 0)))

	def test__game_object_at__returns_game_object(self):
		alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask.fill((255, 255, 255, 255))
		self.clickmap.mark_game_object('obj1', (0, 0), alpha_mask)
		self.assertEqual(self.clickmap.game_object_at((0, 0)), 'obj1')

	def test__game_object_at__handles_overlaps(self):
		alpha_mask1 = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask1.fill((255, 255, 255, 255))
		alpha_mask2 = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask2.fill((255, 255, 255, 255))
		self.clickmap.mark_game_object('obj1', (0, 0), alpha_mask1)
		self.clickmap.mark_game_object('obj2', (5, 5), alpha_mask2)
		self.assertEqual(self.clickmap.game_object_at((0, 0)), 'obj1')
		self.assertEqual(self.clickmap.game_object_at((6, 6)), 'obj2')

	def test__game_object_at__obstructed_by_terrain(self):
		gobj_alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		gobj_alpha_mask.fill((255, 255, 255, 255))
		terrain_alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		terrain_alpha_mask.fill((0, 0, 0, 255))
		self.clickmap.mark_game_object('obj1', (0, 0), gobj_alpha_mask)
		self.clickmap.mark_terrain((0, 5), terrain_alpha_mask)
		self.assertEqual(self.clickmap.is_terrain((0, 5)), True)

	def test__clear__clears(self):
		alpha_mask = pygame.Surface((10, 10), pygame.SRCALPHA)
		alpha_mask.fill((255, 255, 255, 255))
		self.clickmap.mark_game_object('obj1', (0, 0), alpha_mask)
		self.assertFalse(self.clickmap.is_terrain((0, 0)))
		self.clickmap.clear()
		self.assertTrue(self.clickmap.is_terrain((0, 0)))

if __name__ == '__main__':
	unittest.main()
