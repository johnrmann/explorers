import unittest

from src.gameobject.interactable import Interactable
from src.gameobject.constants import NO_OWNER

class _Widget(Interactable):
	"""Stub class to test ownership!"""

class InteractableTest(unittest.TestCase):
	def test__default_no_owner(self):
		w = _Widget()
		self.assertEqual(w.owner, NO_OWNER)

	def test__is_interactable__anyone_if_no_owner(self):
		w = _Widget()
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertTrue(w.is_interactable_by_player(2))
		self.assertTrue(w.is_interactable_by_player(3))
	
	def test__is_interactable__only_owner_if_not_shared(self):
		w = _Widget()
		w.owner = 1
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertFalse(w.is_interactable_by_player(2))
		self.assertFalse(w.is_interactable_by_player(3))

	def test__is_interactable__sharing(self):
		w = _Widget()
		w.owner = 1
		w.shared_with.add(3)
		self.assertTrue(w.is_interactable_by_player(1))
		self.assertFalse(w.is_interactable_by_player(2))
		self.assertTrue(w.is_interactable_by_player(3))

if __name__ == '__main__':
	unittest.main()
