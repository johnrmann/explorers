import unittest

from src.math.adj import adj_cells
from src.math.smooth import smooth_matrix

TEST_MAT = [
	[0,0,0],
	[0,1,0],
	[0,0,0],
]

TEST_LOOP_MAT = [
	[0,0,0],
	[1,0,0],
	[0,0,0],
]

class SmoothMatrixTest(unittest.TestCase):
	def sanity__correct_adj(self):
		d = (3,3)
		self.assertEqual(
			len(adj_cells(d, (1,1), diag=True)),
			8
		)
	
	def test__smooth_matrix__noop(self):
		result = smooth_matrix(TEST_MAT, weight = 0)
		for y in range(3):
			for x in range(3):
				if x == y == 1:
					self.assertEqual(result[y][x], 1)
				else:
					self.assertEqual(result[y][x], 0)

if __name__ == "__main__":
	unittest.main()
