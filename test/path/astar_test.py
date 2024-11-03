import unittest

from src.world.world import World
from src.world.terrain import Terrain

from src.path.astar import astar

class AstarTest(unittest.TestCase):
	def _make_world(self, matrix):
		terrain = Terrain(matrix)
		world = World(terrain)
		return world
	
	def test__astar__trivial(self):
		world = self._make_world([
			[1, 2, 3, 9, 9, 9],
			[2, 3, 4, 9, 9, 9],
			[3, 4, 5, 9, 9, 9],
		])

		start = (0, 0)
		goal = (1, 0)
		exp_path = [(0, 0), (1,0)]

		path = astar(world, start, goal)
		self.assertEqual(path, exp_path)
	
	def test__astar__columbus_case(self):
		world = self._make_world([
			[1, 9, 9, 9, 1, 1],
			[9, 9, 9, 9, 1, 9],
			[9, 9, 9, 9, 9, 9],
		])

		start = (0, 0)
		goal = (4, 0)
		exp_path = [(0, 0), (5,0), (4, 0)]

		path = astar(world, start, goal)
		self.assertEqual(path, exp_path)
	
	def test__astar__columbus_case2(self):
		world = self._make_world([
			[1, 9, 9, 9, 1, 1],
			[9, 9, 9, 9, 1, 9],
			[9, 9, 9, 9, 9, 9],
		])

		start = (0, 0)
		goal = (4, 1)
		exp_path = [(0, 0), (5, 0), (4, 0), (4, 1)]

		path = astar(world, start, goal)
		self.assertEqual(path, exp_path)

	def test__astar__simple_path(self):
		world = self._make_world([
			[1, 2, 3, 9, 9, 9],
			[2, 3, 4, 9, 9, 9],
			[3, 4, 5, 9, 9, 9],
		])

		start = (0, 0)
		goal = (2, 2)
		exp_path = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]

		path = astar(world, start, goal)
		self.assertEqual(path, exp_path)

if __name__ == "__main__":
	unittest.main()
