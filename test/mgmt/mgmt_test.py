import unittest

from unittest.mock import MagicMock, call

from src.mgmt.game_manager import GameManager, TICKS_PER_SECOND

from test.mgmt.test_objects import (
	Rocket,
	Launchpad,
	Moon,
	OmniListener
)

class MgmtTest(unittest.TestCase):
	def test__launch(self):
		game_mgr = GameManager(None, None)

		# BeginCareful - order matters for assert calls.
		launchpad = Launchpad()
		rocket = Rocket()
		moon = Moon()
		omni = OmniListener(rocket.evt_mgr)
		# EndCareful

		game_mgr.game_objects.append(launchpad)
		game_mgr.game_objects.append(moon)
		game_mgr.game_objects.append(rocket)

		mock_update = omni.update = MagicMock()
		launchpad.launch()
		for _ in range(0, 10):
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
			call('rocket_arrive', None),
			call('rocket_cruise', 10.0),
		])
