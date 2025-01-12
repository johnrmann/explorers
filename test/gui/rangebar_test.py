import unittest
import pygame

from src.gui.rangebar import Rangebar, HEALTH_LAYERS
from test.gui.setup import make_mock_gui_manager

class TestRangebar(unittest.TestCase):

	def test__init__raises_ValueError_when_no_rect(self):
		with self.assertRaises(ValueError):
			Rangebar()

	def test__init__default_layers(self):
		rect = ((0, 0), (100, 20))
		rangebar = Rangebar(rect=rect, gui_mgr=make_mock_gui_manager())
		self.assertEqual(rangebar.layers, HEALTH_LAYERS)

	def test__init__default_values(self):
		rect = ((0, 0), (100, 20))
		rangebar = Rangebar(rect=rect, gui_mgr=make_mock_gui_manager())
		expected_values = [(low + hi) // 2 for _, low, hi in HEALTH_LAYERS[1:]]
		self.assertEqual(rangebar.values, expected_values)

	def test__pygame_rect(self):
		rect = ((10, 10), (200, 30))
		rangebar = Rangebar(rect=rect, gui_mgr=make_mock_gui_manager())
		expected_pygame_rect = pygame.Rect(10, 10, 200, 30)
		self.assertEqual(rangebar.pygame_rect, expected_pygame_rect)

	def test__draw(self):
		rect = ((0, 0), (100, 20))
		screen = pygame.Surface((100, 20))
		layers = [
			(pygame.Color(0, 0, 255), 0, 0),
			(pygame.Color(0, 255, 0), 0, 100)
		]
		values = [50]
		rangebar = Rangebar(
			rect=rect,
			layers=layers,
			values=values,
			gui_mgr=make_mock_gui_manager()
		)
		rangebar.draw(screen)
		self.assertEqual(screen.get_at((70, 10)), pygame.Color(0, 0, 255))
		self.assertEqual(screen.get_at((20, 10)), pygame.Color(0, 255, 0))

if __name__ == '__main__':
	unittest.main()
