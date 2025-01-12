import unittest

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager

from src.gui.gui import _GuiManager
from src.gui.mission_clock import MissionClock
from test.gui.setup import make_mock_gui_manager

class TestMissionClock(unittest.TestCase):

	def test__initial_mode(self):
		mission_clock = MissionClock(
			gui_mgr=make_mock_gui_manager()
		)
		self.assertEqual(mission_clock.button.text, "UTC")
		self.assertEqual(mission_clock.label.text, "2351-01-01")

	def test__toggle_mode(self):
		mission_clock = MissionClock(
			gui_mgr=make_mock_gui_manager()
		)
		mission_clock.on_click_clock_mode()
		self.assertEqual(mission_clock.button.text, "MT")
		self.assertEqual(mission_clock.label.text, "001-001")

		mission_clock.on_click_clock_mode()
		self.assertEqual(mission_clock.button.text, "UTC")
		self.assertEqual(mission_clock.label.text, "2351-01-01")

if __name__ == '__main__':
	unittest.main()
