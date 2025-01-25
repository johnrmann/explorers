import unittest

from src.player.player import Player

class PlayerTest(unittest.TestCase):
	def test__init__with_uid(self):
		"""Test that we can create a player with a valid UID."""
		uid = 1
		player = Player(uid)
		self.assertEqual(player.uid, uid)


	def test__init__rejects_none_uid(self):
		"""Test that we cannot create a player with a None UID."""
		with self.assertRaises(ValueError):
			Player(None)


	def test__init__rejects_zero_uid(self):
		"""Test that we cannot create a player with a zero (wildcard) UID."""
		with self.assertRaises(ValueError):
			Player(0)


	def test__equals__true_with_same_object(self):
		"""Test that a player is equal to itself."""
		player = Player(1)
		self.assertTrue(player == player)


	def test__equals__true_with_same_uid(self):
		"""Test the UID shortcut for equality."""
		player1 = Player(1)
		self.assertTrue(player1 == 1)


	def test__equals__true_with_wildcard_uid(self):
		"""Test that a player is equal to the wildcard UID."""
		player1 = Player(1)
		self.assertTrue(player1 == 0)


	def test__equals__false_with_different_uid(self):
		"""Test that players with different UIDs are not equal."""
		player1 = Player(1)
		self.assertFalse(player1 == 2)


	def test__equals__false_with_string(self):
		"""Test that a player is not equal to None."""
		player1 = Player(1)
		self.assertFalse(player1 == "player1")



if __name__ == '__main__':
	unittest.main()
