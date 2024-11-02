import unittest

from src.math.adj import *

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
for p in range(3):
	q = p + 1
	SIMPLE_B_ADJ[p][q] = True
	SIMPLE_B_ADJ[q][p] = True

class AdjTest(unittest.TestCase):
	def test__adj_cells__normie(self):
		d = (3,3)
		p = (1,1)
		self.assertEqual(
			adj_cells(d, p, loop_x=False),
			[(0, 1), (1, 0), (1, 2), (2, 1)]
		)
	
	def test__adj_cells__loop_x(self):
		d = (3,3)
		p = (0,1)
		self.assertEqual(
			adj_cells(d, p, loop_x=True),
			[(2, 1), (0, 0), (0, 2), (1, 1)]
		)
	
	def test__adj_cells__bound_y(self):
		d = (3,3)
		p = (1,0)
		self.assertEqual(
			adj_cells(d, p, loop_x=False, loop_y=False),
			[(0, 0), (1, 1), (2, 0)]
		)
		p = (1,2)
		self.assertEqual(
			adj_cells(d, p, loop_x=False, loop_y=False),
			[(0, 2), (1, 1), (2, 2)]
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

if __name__ == "__main__":
	unittest.main()
