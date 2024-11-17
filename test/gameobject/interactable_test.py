import unittest

from unittest.mock import MagicMock

from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager

from src.gameobject.interactable import Interactable
from src.gameobject.constants import NO_OWNER

class _Widget(Interactable):
	"""Stub class to test ownership!"""

class InteractableTest(unittest.TestCase):
	def setUp(self):
		evt_mgr = MagicMock(spec=EventManager)
		game_mgr = MagicMock(spec=GameManager)
		game_mgr.evt_mgr = evt_mgr
		self.w = _Widget(game_mgr=game_mgr)

	def test__default_no_owner(self):
		w = self.w
		self.assertEqual(w.owner, NO_OWNER)

	def test__is_interactable__anyone_if_no_owner(self):
		w = self.w
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertTrue(w.is_interactable_by_player(2))
		self.assertTrue(w.is_interactable_by_player(3))

	def test__is_interactable__only_owner_if_not_shared(self):
		w = self.w
		w.owner = 1
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertFalse(w.is_interactable_by_player(2))
		self.assertFalse(w.is_interactable_by_player(3))

	def test__is_interactable__sharing(self):
		w = self.w
		w.owner = 1
		w.shared_with.add(3)
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertFalse(w.is_interactable_by_player(2))
		self.assertTrue(w.is_interactable_by_player(3))

if __name__ == '__main__':
	unittest.main()
