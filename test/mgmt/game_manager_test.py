import unittest

from src.mgmt.game_manager import GameManager

from unittest.mock import MagicMock, call

class GameManagerTest(unittest.TestCase):
	def test__utc(self):
		"""Test that UTC changes with the flow of time."""
		gm = GameManager(None, None)
		self.assertEqual(gm.utc, 0)
		gm.tick(1)
		self.assertEqual(gm.utc, 1 / 25)
		gm.tick(24)
		self.assertEqual(gm.utc, 1)
	
	def test__rejects_time_travel(self):
		"""Ensure that an error is thrown if we try to tick with a negative
		dt."""
		gm = GameManager(None, None)
		self.assertRaises(ValueError, lambda: gm.tick(-1))

if __name__ == "__main__":
	unittest.main()
