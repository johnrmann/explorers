import unittest

from unittest.mock import MagicMock

from math import modf

from src.gameobject.actor import Actor
from src.math.vector2 import Vector2

CARDINAL_PATH = [
	Vector2(0,0),
	Vector2(0,1),
	Vector2(1,1),
]

class ActorTest(unittest.TestCase):
	def test__moves_on_path(self):
		actor = Actor(speed=1)
		actor._path_runner.path = (CARDINAL_PATH)
		check_idx = 0
		while actor.is_moving:
			self.assertEqual(actor.pos, CARDINAL_PATH[check_idx])
			actor.tick(1, check_idx)
			check_idx += 1

	def test__dies_when_hunger_depletes(self):
		actor = Actor(speed=1)
		actor.motives.hunger = 10
		while actor.motives.hunger > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())

	def test__dies_when_oxygen_depletes(self):
		actor = Actor(speed=1)
		actor.motives.oxygen = 10
		while actor.motives.oxygen > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())

	def test__evt_mgr_gets_died_from_hunger(self):
		actor = Actor(speed=1)
		actor.motives.hunger = 10
		actor.evt_mgr = MagicMock()
		while actor.motives.hunger > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())
		actor.evt_mgr.pub.assert_called_with("character.died", actor)

	def test__evt_mgr_gets_died_from_oxygen(self):
		actor = Actor(speed=1)
		actor.motives.oxygen = 10
		actor.evt_mgr = MagicMock()
		while actor.motives.oxygen > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())
		actor.evt_mgr.pub.assert_called_with("character.died", actor)

	def test__motives_decrease_over_time(self):
		actor = Actor(speed=1)
		initial_hunger = actor.motives.hunger
		initial_oxygen = actor.motives.oxygen
		actor.tick(1, 0)
		self.assertLess(actor.motives.hunger, initial_hunger)
		self.assertLess(actor.motives.oxygen, initial_oxygen)

	def test__motives_decrease_faster_when_moving(self):
		actor = Actor(speed=1)
		actor._path_runner.path = CARDINAL_PATH
		o2_init, hunger_init, _, _ = actor.motives
		actor.tick(1, 0)
		o2_mvmt, hunger_mvmt, _, _ = actor.motives

		actor.motives.hunger = o2_init
		actor.motives.oxygen = hunger_init
		actor._path_runner.path = None

		actor.tick(1, 0)
		o2_still, hunger_still, _, _ = actor.motives

		self.assertLess(hunger_mvmt, hunger_still)
		self.assertLess(o2_mvmt, o2_still)

if __name__ == "__main__":
	unittest.main()

if __name__ == "__main__":
	unittest.main()
