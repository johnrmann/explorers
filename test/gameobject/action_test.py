import unittest

from src.math.vector2 import Vector2
from src.gameobject.action import Action

class MockTarget:
	def __init__(self, pos):
		self.pos = pos

class ActionTest(unittest.TestCase):
	def test__position__no_offset(self):
		target = MockTarget(Vector2(10, 20))
		action = Action(target=target)
		self.assertEqual(action.position, Vector2(10, 20))

	def test__position__with_offset(self):
		target = MockTarget(Vector2(10, 20))
		offset = Vector2(5, 5)
		action = Action(target=target, offset=offset)
		self.assertEqual(action.position, Vector2(15, 25))

if __name__ == '__main__':
	unittest.main()
