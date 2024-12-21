import unittest
from unittest.mock import MagicMock
import pygame
from src.gui.playbar import Playbar, PlaybarMode
from src.gui.primitives import Panel

class TestPlaybar(unittest.TestCase):

	def setUp(self):
		self.game_mock = MagicMock()
		self.game_mock.world = MagicMock()
		self.game_mock.world.terrain = MagicMock()
		self.game_mock.world.terrain.dimensions = (64, 64)
		self.game_mock.renderer.vp.window_dims = (800, 600)
		self.playbar = Playbar(self.game_mock)

	def test__init__initial_mode_is_character(self):
		self.assertEqual(self.playbar.mode, PlaybarMode.CHARACTER)

	def test__init__panel_is_not_hidden(self):
		self.assertFalse(self.playbar._panel.hidden)

	def test__mode_setter__changes_mode(self):
		self.playbar.mode = PlaybarMode.PLANET
		self.assertEqual(self.playbar.mode, PlaybarMode.PLANET)

	def test__mode_setter__hides_previous_mode_elements(self):
		self.playbar.mode = PlaybarMode.PLANET
		for elem in self.playbar._mode_to_elements[PlaybarMode.CHARACTER]:
			self.assertTrue(elem.hidden)

	def test__mode_setter__unhides_new_mode_elements(self):
		self.playbar.mode = PlaybarMode.PLANET
		for elem in self.playbar._mode_to_elements[PlaybarMode.PLANET]:
			self.assertFalse(elem.hidden)

	def test__process_event__changes_mode_on_keypress(self):
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2)
		self.playbar.process_event(event)
		self.assertEqual(self.playbar.mode, PlaybarMode.PLANET)

	def test__process_event__returns_true_on_valid_keypress(self):
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2)
		result = self.playbar.process_event(event)
		self.assertTrue(result)

	def test__process_event__returns_false_on_invalid_keypress(self):
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F5)
		result = self.playbar.process_event(event)
		self.assertFalse(result)

if __name__ == '__main__':
	unittest.main()