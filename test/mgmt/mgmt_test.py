import unittest

from unittest.mock import MagicMock, call, patch

from src.render.viewport import Viewport

from src.mgmt.game_manager import GameManager, TICKS_PER_SECOND
from test.mgmt.test_objects import (
	Rocket,
	Launchpad,
	Moon,
	OmniListener
)

class MgmtTest(unittest.TestCase):

	@patch('src.mgmt.singletons.get_game_manager')
	def setUp(self, mock_get_game_manager):
		self.viewport = MagicMock(spec=Viewport)
		self.viewport.window_dims = (800, 600)
		self.game_mgr = GameManager(None, self.viewport)
		mock_get_game_manager.return_value = self.game_mgr

	def test__launch(self):
		game_mgr = self.game_mgr

		# BeginCareful - order matters for assert calls.
		launchpad = Launchpad(game_mgr=game_mgr)
		rocket = Rocket(game_mgr=game_mgr)
		moon = Moon(game_mgr=game_mgr)
		omni = OmniListener(rocket.evt_mgr)
		# EndCareful

		game_mgr.game_objects.append(launchpad)
		game_mgr.game_objects.append(moon)
		game_mgr.game_objects.append(rocket)

		mock_update = omni.update = MagicMock()
		launchpad.launch()
		for _ in range(0, 12):
			game_mgr.tick(TICKS_PER_SECOND)
		mock_update.assert_has_calls([
			call('rocket_launch', None),
			call('rocket_cruise', 1.0),
			call('rocket_cruise', 2.0),
			call('rocket_cruise', 3.0),
			call('rocket_cruise', 4.0),
			call('rocket_cruise', 5.0),
			call('rocket_cruise', 6.0),
			call('rocket_cruise', 7.0),
			call('rocket_cruise', 8.0),
			call('rocket_cruise', 9.0),
			call('rocket_cruise', 10.0),
			call('rocket_arrive', None),
		])
