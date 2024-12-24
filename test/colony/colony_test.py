import unittest

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager

from src.colony.colony import Colony, COLONY_NAMES

class ColonyTest(unittest.TestCase):
	def setUp(self):
		self.game_mgr = MagicMock(spec=GameManager)
		self.game_mgr.world = MagicMock()
		self.game_mgr.world.width = 128
		self.game_mgr.world.height = 128
		self.game_mgr.is_single_player = True

	def test__init__raises_error_if_owner_is_none(self):
		with self.assertRaises(ValueError):
			Colony(owner=None, position=(0, 0), game_mgr=self.game_mgr)

	def test__init__raises_error_if_owner_is_zero(self):
		with self.assertRaises(ValueError):
			Colony(owner=0, position=(0,0), game_mgr=self.game_mgr)

	def test__init__raises_error_if_position_is_none(self):
		with self.assertRaises(ValueError):
			Colony(owner=1, position=None, game_mgr=self.game_mgr)

	def test__init__sets_owner(self):
		colony = Colony(owner=1, position=(0, 0), game_mgr=self.game_mgr)
		self.assertEqual(colony.owner, 1)

	def test__init__sets_name_to_single_player_default(self):
		colony = Colony(
			owner=1,
			position=(0, 0),
			game_mgr=self.game_mgr,
			is_first=True
		)
		self.assertEqual(colony.name, "First Landing")

	def test__init__sets_name_to_multi_player_default(self):
		self.game_mgr.is_single_player = False
		colony = Colony(
			owner=2,
			position=(0, 0),
			game_mgr=self.game_mgr,
			is_first=True
		)
		self.assertEqual(colony.name, "Outpost Beta")

	def test__init__sets_name_to_custom(self):
		colony = Colony(
			owner=1,
			position=(0, 0),
			game_mgr=self.game_mgr,
			name="Buena Vista"
		)
		self.assertEqual(colony.name, "Buena Vista")

	def test__init__chooses_name_from_list(self):
		colony = Colony(
			owner=1,
			position=(0, 0),
			game_mgr=self.game_mgr
		)
		self.assertIn(colony.name, COLONY_NAMES)

if __name__ == '__main__':
	unittest.main()
