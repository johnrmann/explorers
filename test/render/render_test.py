import unittest
import pygame

from unittest.mock import Mock, MagicMock

from src.render.render import Render

from test.setups import make_basic_game_manager


class RenderTest(unittest.TestCase):
	def setUp(self):
		self.window = pygame.Surface((800, 600))
		self.game_mgr = make_basic_game_manager()
		self.render = Render(
			self.window,
			self.game_mgr.world,
			self.game_mgr.vp,
			self.game_mgr,
		)


	def test__highlight_tile__works(self):
		self.render.highlight_tile((4, 8), color=(255, 0, 0))
		self.assertEqual(
			self.render._highlight_colors[(4, 8)],
			(1, (255, 0, 0))
		)


	def test__highlight_tile__overwrites(self):
		self.render.highlight_tile((4, 8), color=(255, 0, 0))
		self.render.highlight_tile((4, 8), color=(0, 255, 0), priority=2)
		self.assertEqual(
			self.render._highlight_colors[(4, 8)],
			(2, (0, 255, 0))
		)


	def test__highlight_tile__higher_priority(self):
		self.render.highlight_tile((4, 8), color=(0, 255, 0), priority=2)
		self.render.highlight_tile((4, 8), color=(255, 0, 0))
		self.assertEqual(
			self.render._highlight_colors[(4, 8)],
			(2, (0, 255, 0))
		)


	def test__highlight_tile__none(self):
		self.render.highlight_tile(None)
		self.assertEqual(
			self.render._highlight_colors[(4, 8)],
			None
		)


	def test__clear__clears_highlights(self):
		self.render.highlight_tile((4, 8), color=(255, 0, 0))
		self.render.clear()
		self.assertEqual(
			self.render._highlight_colors[(4, 8)],
			None
		)



if __name__ == '__main__':
	unittest.main()
