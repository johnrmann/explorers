import unittest

from src.math.direction import Direction
from src.math.vector2 import Vector2
from src.math.adj import (
	adj_cells,
	keyed_adj_cells,
	bool_adj_from_labels,
	select_adj_degree,
	are_cells_adj_cardinally,
	are_cells_adj,
	are_cells_adj_diagonally
)

EXAMPLE_ADJ = [
	[0,0,1,1],
	[0,0,1,2],
	[3,4,2,2],
	[5,5,5,5],
]

EXAMPLE_ADJ_PAIRS = [
	(0, 1),
	(0, 3),
	(0, 4),
	(1, 2),
	(3, 5),
	(3, 4),
	(2, 5),
	(2, 4),
	(4, 5)
]

SIMPLE_B_ADJ = [[False] * 4 for i in range(4)]
for a in range(3):
	b = a + 1
	SIMPLE_B_ADJ[a][b] = True
	SIMPLE_B_ADJ[b][a] = True

class AdjTest(unittest.TestCase):
	def test__keyed_adj_cells__normie(self):
		d = (3,3)
		p = (1,1)
		result = keyed_adj_cells(d, p, loop_x=False)
		self.assertEqual(result[Direction.NORTH],(1,0))
		self.assertEqual(result[Direction.EAST],(2,1))
		self.assertEqual(result[Direction.SOUTH],(1,2))
		self.assertEqual(result[Direction.WEST],(0,1))
	
	def test__adj_cells__normie(self):
		d = (3,3)
		p = (1,1)
		self.assertEqual(
			adj_cells(d, p, loop_x=False),
			[(1, 0), (2, 1), (1, 2), (0, 1)]
		)
	
	def test__adj_cells__loop_x(self):
		d = (3,3)
		p = (0,1)
		self.assertEqual(
			adj_cells(d, p, loop_x=True),
			[(0, 0), (1, 1), (0, 2), (2, 1)]
		)
	
	def test__adj_cells__bound_y(self):
		d = (3,3)
		p = (1,0)
		self.assertEqual(
			adj_cells(d, p, loop_x=False, loop_y=False),
			[(2, 0), (1, 1), (0, 0)]
		)
		p = (1,2)
		self.assertEqual(
			adj_cells(d, p, loop_x=False, loop_y=False),
			[(1, 1), (2, 2), (0, 2)]
		)
	
	def test__bool_adj_from_labels__normie(self):
		ans = bool_adj_from_labels(EXAMPLE_ADJ, 6, loop_x=False, loop_y=False)
		adj_pairs = EXAMPLE_ADJ_PAIRS

		for y in range(6):
			for x in range(6):
				if (x, y) in adj_pairs or (y, x) in adj_pairs:
					self.assertTrue(ans[y][x])
				else:
					self.assertFalse(ans[y][x])

	def test__bool_adj_from_labels__loop_x(self):
		ans = bool_adj_from_labels(EXAMPLE_ADJ, 6, loop_x=True, loop_y=False)
		adj_pairs = EXAMPLE_ADJ_PAIRS[:] + [
			(0, 2),
			(3, 2),
		]

		for y in range(6):
			for x in range(6):
				if (x, y) in adj_pairs or (y, x) in adj_pairs:
					self.assertTrue(ans[y][x])
				else:
					self.assertFalse(ans[y][x])
	
	def test__select_adj_degree__base(self):
		self.assertEqual(
			select_adj_degree(SIMPLE_B_ADJ, 0, 0),
			set([0])
		)
	
	def test__select_adj_degree__neighbors(self):
		self.assertEqual(
			select_adj_degree(SIMPLE_B_ADJ, 0, 1),
			set([0, 1])
		)
	
	def test__select_adj_degree__neighbors_neighbors(self):
		self.assertEqual(
			select_adj_degree(SIMPLE_B_ADJ, 0, 2),
			set([0, 1, 2])
		)
	
	def test__select_adj_degree__spread(self):
		self.assertEqual(
			select_adj_degree(SIMPLE_B_ADJ, 1, 2),
			set([0, 1, 2, 3])
		)

	def test__are_cells_adj_cardinally__true(self):
		p = Vector2(1, 1)
		q = Vector2(1, 2)
		self.assertTrue(are_cells_adj_cardinally(p, q))
		q = Vector2(2, 1)
		self.assertTrue(are_cells_adj_cardinally(p, q))

	def test__are_cells_adj_cardinally__false(self):
		p = Vector2(1, 1)
		q = Vector2(2, 2)
		self.assertFalse(are_cells_adj_cardinally(p, q))
		q = Vector2(0, 0)
		self.assertFalse(are_cells_adj_cardinally(p, q))

	def test__are_cells_adj_diagonally__true(self):
		p = Vector2(1, 1)
		q = Vector2(2, 2)
		self.assertTrue(are_cells_adj_diagonally(p, q))
		q = Vector2(0, 0)
		self.assertTrue(are_cells_adj_diagonally(p, q))

	def test__are_cells_adj_diagonally__false(self):
		p = Vector2(1, 1)
		q = Vector2(1, 2)
		self.assertFalse(are_cells_adj_diagonally(p, q))
		q = Vector2(2, 1)
		self.assertFalse(are_cells_adj_diagonally(p, q))

	def test__are_cells_adj__cardinal(self):
		p = Vector2(1, 1)
		q = Vector2(1, 2)
		self.assertTrue(are_cells_adj(p, q))
		q = Vector2(2, 1)
		self.assertTrue(are_cells_adj(p, q))

	def test__are_cells_adj__diagonal(self):
		p = Vector2(1, 1)
		q = Vector2(2, 2)
		self.assertTrue(are_cells_adj(p, q))
		q = Vector2(0, 0)
		self.assertTrue(are_cells_adj(p, q))

	def test__are_cells_adj__false(self):
		p = Vector2(1, 1)
		q = Vector2(2, 3)
		self.assertFalse(are_cells_adj(p, q))
		q = Vector2(-4, 2)
		self.assertFalse(are_cells_adj(p, q))

if __name__ == "__main__":
	unittest.main()
