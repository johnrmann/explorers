import unittest

from src.world.terrain import Terrain

from src.path.astar import astar

# These are convenient for making compact accessibility matrices. Don't map
# anything to `_`.
X = True
_ = False

def _make_accessibility_func(matrix):
	def is_cell_occupied(cell):
		x, y = cell
		return matrix[y][x] == True
	return is_cell_occupied

class AstarTest(unittest.TestCase):
	def _make_terrain(self, matrix):
		terrain = Terrain(matrix)
		return terrain

	def test__astar__trivial(self):
		terrain = self._make_terrain([
			[1, 2, 3, 9, 9, 9],
			[2, 3, 4, 9, 9, 9],
			[3, 4, 5, 9, 9, 9],
		])

		start = (0, 0)
		goal = (1, 0)
		exp_path = [(0, 0), (1,0)]

		path = astar(start, goal, terrain)
		self.assertEqual(path, exp_path)

	def test__astar__columbus_case(self):
		terrain = self._make_terrain([
			[1, 9, 9, 9, 1, 1],
			[9, 9, 9, 9, 1, 9],
			[9, 9, 9, 9, 9, 9],
		])

		start = (0, 0)
		goal = (4, 0)
		exp_path = [(0, 0), (5,0), (4, 0)]

		path = astar(start, goal, terrain)
		self.assertEqual(path, exp_path)

	def test__astar__columbus_case2(self):
		terrain = self._make_terrain([
			[1, 9, 9, 9, 1, 1],
			[9, 9, 9, 9, 1, 9],
			[9, 9, 9, 9, 9, 9],
		])

		start = (0, 0)
		goal = (4, 1)
		exp_path = [(0, 0), (5, 0), (4, 0), (4, 1)]

		path = astar(start, goal, terrain)
		self.assertEqual(path, exp_path)

	def test__astar__simple_path(self):
		terrain = self._make_terrain([
			[1, 2, 3, 9, 9, 9],
			[2, 3, 4, 9, 9, 9],
			[3, 4, 5, 9, 9, 9],
		])

		start = (0, 0)
		goal = (2, 2)
		exp_path = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]

		path = astar(start, goal, terrain)
		self.assertEqual(path, exp_path)

	def test__astar__inaccessible_goal(self):
		terrain = self._make_terrain([
			[1, 2, 3, 9, 9, 9],
			[2, 3, 4, 9, 9, 9],
			[3, 4, 5, 9, 9, 9],
		])
		access = _make_accessibility_func([
			[_, _, _, _, _, _],
			[_, _, _, _, _, _],
			[_, _, X, _, _, _],
		])

		start = (0, 0)
		goal = (2, 2)
		exp_path = []

		path = astar(start, goal, terrain, access)
		self.assertEqual(path, exp_path)

	def test__astar__inaccessible_indirectly(self):
		terrain = self._make_terrain([
			[1] * 6,
			[1] * 6,
			[1] * 6,
		])
		access = _make_accessibility_func([
			[_] * 6,
			[X] * 6,
			[_] * 6,
		])

		start = (0, 0)
		goal = (2, 2)
		exp_path = []

		path = astar(start, goal, terrain, access)
		self.assertEqual(path, exp_path)

if __name__ == "__main__":
	unittest.main()
