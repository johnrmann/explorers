import unittest
from unittest.mock import MagicMock, Mock, patch
import pygame
from src.gui.playbar import Playbar, PlaybarMode
from src.gui.primitives import Panel

from test.gui.setup import make_mock_gui_manager

class TestPlaybar(unittest.TestCase):

	@patch('src.gui.playbar.Scanline', autospec=True)
	@patch('src.gui.playbar.LineGraph', autospec=True)
	@patch('src.gui.playbar.ImageButtonGrid', autospec=True)
	@patch('src.gui.playbar.Catalog', autospec=True)
	def setUp(self, MockScanline, MockLineGraph, MockImageButtonGrid, MockCatalog):
		MockScanline.return_value = Mock()
		MockLineGraph.return_value = Mock()
		MockImageButtonGrid.return_value = Mock()
		MockCatalog.return_value = Mock()
		self.change_mode_callback = Mock()
		self.gui_mgr = make_mock_gui_manager()
		self.playbar = Playbar(
			self.gui_mgr.game_mgr,
			change_mode_callback=self.change_mode_callback,
			gui_mgr=self.gui_mgr,
			evt_mgr=self.gui_mgr.game_mgr.evt_mgr
		)

	def test__init__initial_mode_is_character(self):
		self.assertEqual(self.playbar.mode, PlaybarMode.CHARACTER)

	def test__init__panel_is_not_hidden(self):
		self.assertFalse(self.playbar._panel.hidden)

	def test__mode_setter__changes_mode(self):
		self.playbar.mode = PlaybarMode.PLANET
		self.assertEqual(self.playbar.mode, PlaybarMode.PLANET)

	def test__mode_setter__calls_callback(self):
		self.playbar.mode = PlaybarMode.PLANET
		self.change_mode_callback.assert_called_once_with(PlaybarMode.PLANET)

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

	def test__process_event__calls_callback(self):
		event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2)
		self.playbar.process_event(event)
		self.change_mode_callback.assert_called_once_with(PlaybarMode.PLANET)

if __name__ == '__main__':
	unittest.main()
