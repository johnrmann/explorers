import unittest

from unittest.mock import MagicMock, call, patch

from src.render.viewport import Viewport

from src.mgmt.game_manager import GameManager, TICKS_PER_SECOND
from test.mgmt.test_objects import (
	Rocket,
	Launchpad,
	Moon,
	OmniListener,
	RocketLaunchEvent,
	RocketCruiseEvent,
	RocketArriveEvent
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
		calls = [
			RocketLaunchEvent(),
			*[
				RocketCruiseEvent(utc)
				for utc in range(1, 11)
			],
			RocketArriveEvent()
		]
		for i in range(len(calls)):
			self.assertEqual(mock_update.call_args_list[i], call(calls[i]))
