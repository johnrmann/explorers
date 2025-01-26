import unittest

from unittest.mock import MagicMock

from src.gameobject.rabbit_hole import RabbitHole
from src.gameobject.gameobject import GameObject



class MyRabbitHole(GameObject, RabbitHole):
	"""A rabbit hole that can hold actors."""

	def __init__(self, max_capacity=1, **kwargs):
		GameObject.__init__(self, **kwargs)
		RabbitHole.__init__(self, max_capacity=max_capacity)



class RabbitHoleTest(unittest.TestCase):
	def setUp(self):
		self.game_mgr = MagicMock()


	def test__init__empty(self):
		"""Test that we can create an empty rabbit hole."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=3)
		self.assertEqual(rabbit_hole.max_capacity, 3)
		self.assertEqual(rabbit_hole.capacity, 3)
		self.assertEqual(rabbit_hole.inside, set())


	def test__enter__true(self):
		"""Test that we can enter a rabbit hole."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=1)
		actor = MagicMock()
		self.assertTrue(rabbit_hole.enter(actor))
		self.assertEqual(rabbit_hole.capacity, 0)
		self.assertEqual(rabbit_hole.inside, {actor})


	def test__enter__false(self):
		"""Test that we cannot enter a full rabbit hole."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=1)
		actor = MagicMock()
		rabbit_hole.enter(actor)
		self.assertFalse(rabbit_hole.enter(MagicMock()))
		self.assertEqual(rabbit_hole.capacity, 0)
		self.assertEqual(rabbit_hole.inside, {actor})


	def test__is_full__true(self):
		"""Test that a full rabbit hole is full."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=1)
		self.assertFalse(rabbit_hole.is_full())
		rabbit_hole.enter(MagicMock())
		self.assertTrue(rabbit_hole.is_full())


	def test__exit__true(self):
		"""Test that we can exit a rabbit hole."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=1)
		actor = MagicMock()
		rabbit_hole.enter(actor)
		self.assertTrue(rabbit_hole.exit(actor))
		self.assertEqual(rabbit_hole.capacity, 1)
		self.assertEqual(rabbit_hole.inside, set())


	def test__exit__false(self):
		"""Test that we cannot exit a rabbit hole if the actor is not inside."""
		rabbit_hole = MyRabbitHole(game_mgr=self.game_mgr, max_capacity=1)
		actor = MagicMock()
		self.assertFalse(rabbit_hole.exit(actor))
		self.assertEqual(rabbit_hole.capacity, 1)
		self.assertEqual(rabbit_hole.inside, set())



if __name__ == '__main__':
	unittest.main()
