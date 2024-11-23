import unittest

import pygame

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager

from src.gui.gui import init_gui_manager
from src.gui.mission_clock import MissionClock, DEFAULT_FUNCTION_MAP

class TestMissionClock(unittest.TestCase):

	def setUp(self):
		pygame.init()
		pygame.display.set_mode((800, 600))
		self.game_mgr = MagicMock(spec=GameManager)
		init_gui_manager(self.game_mgr)
		self.mission_clock = MissionClock()

	def tearDown(self):
		del self.mission_clock

	def test__initial_mode(self):
		self.assertEqual(self.mission_clock._mode_idx, 0)
		self.assertEqual(self.mission_clock.get_button_text(0), "UTC")
		self.assertEqual(self.mission_clock.get_label_text(0), "2469-08-20")

	def test__toggle_mode(self):
		self.mission_clock.on_click_clock_mode()
		self.assertEqual(self.mission_clock.get_button_text(0), "MT")
		self.assertEqual(self.mission_clock.get_label_text(0), "001-001")

		self.mission_clock.on_click_clock_mode()
		self.assertEqual(self.mission_clock.get_button_text(0), "UTC")
		self.assertEqual(self.mission_clock.get_label_text(0), "2469-08-20")

	def test__custom_entries(self):
		custom_entries = [
			("Custom1", lambda _: "1994-03-27"),
			("Custom2", lambda _: "1789-11-21")
		]
		mission_clock_custom = MissionClock(entries=custom_entries)
		self.assertEqual(mission_clock_custom.get_button_text(0), "Custom1")
		self.assertEqual(mission_clock_custom.get_label_text(0), "1994-03-27")

		mission_clock_custom.on_click_clock_mode()
		self.assertEqual(mission_clock_custom.get_button_text(0), "Custom2")
		self.assertEqual(mission_clock_custom.get_label_text(0), "1789-11-21")

if __name__ == '__main__':
	unittest.main()