import unittest

import pygame

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager

from src.gui.gui import init_gui_manager
from src.gui.mission_clock import MissionClock

class TestMissionClock(unittest.TestCase):

	def setUp(self):
		pygame.init()
		pygame.display.set_mode((800, 600))
		self.game_mgr = MagicMock(spec=GameManager)
		self.game_mgr.evt_mgr = MagicMock(spec=EventManager)
		self.game_mgr.utc = 0
		self.game_mgr.epoch = (2350 * 360)
		init_gui_manager(self.game_mgr)
		self.mission_clock = MissionClock()

	def tearDown(self):
		del self.mission_clock

	def test__initial_mode(self):
		self.assertEqual(self.mission_clock.button.text, "UTC")
		self.assertEqual(self.mission_clock.label.text, "2351-01-01")

	def test__toggle_mode(self):
		self.mission_clock.on_click_clock_mode()
		self.assertEqual(self.mission_clock.button.text, "MT")
		self.assertEqual(self.mission_clock.label.text, "001-001")

		self.mission_clock.on_click_clock_mode()
		self.assertEqual(self.mission_clock.button.text, "UTC")
		self.assertEqual(self.mission_clock.label.text, "2351-01-01")

if __name__ == '__main__':
	unittest.main()
