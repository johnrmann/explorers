import unittest

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
			actor.act(1)
			check_idx += 1

if __name__ == "__main__":
	unittest.main()
