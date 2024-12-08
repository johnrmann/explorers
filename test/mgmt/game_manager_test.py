import unittest

from src.world.terrain import Terrain
from src.world.world import World
from src.render.viewport import Viewport

from src.mgmt.game_manager import GameManager

from unittest.mock import MagicMock, call

class GameManagerTest(unittest.TestCase):
	def setUp(self):
		self.viewport = MagicMock(spec=Viewport)
		self.viewport.window_dims = (800, 600)
		self.terrain = MagicMock(spec=Terrain)
		self.world = MagicMock(spec=World)
		self.world.terrain = self.terrain

	def test__utc(self):
		"""Test that UTC changes with the flow of time."""
		gm = GameManager(self.world, self.viewport)
		self.assertEqual(gm.utc, 0)
		gm.tick(1 / 50)
		self.assertEqual(gm.utc, 1 / 50)
		gm.tick(49 / 50)
		self.assertEqual(gm.utc, 1)
	
	def test__rejects_time_travel(self):
		"""Ensure that an error is thrown if we try to tick with a negative
		dt."""
		gm = GameManager(self.world, self.viewport)
		self.assertRaises(ValueError, lambda: gm.tick(-1))

if __name__ == "__main__":
	unittest.main()
