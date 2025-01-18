import unittest

from src.math.adj import adj_cells
from src.math.matrix import smooth_matrix, round_matrix_to_int

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

TEST_FLOAT_MAT = [
	[0.333, 0.666, 0.333],
	[0.250, 1.250, 0.250],
	[0.000, 0.999, 0.001]
]

class SmoothMatrixTest(unittest.TestCase):
	def test__sanity__correct_adj(self):
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


	def test__smooth_matrix__edge_no_loop(self):
		result = smooth_matrix(
			TEST_LOOP_MAT, weight = 1, loop_x = False, loop_y = False
		)
		self.assertEqual(result[1][2], 0)


	def test__smooth_matrix__edge_loop(self):
		result = smooth_matrix(
			TEST_LOOP_MAT, weight = 1, loop_x = True, loop_y = False
		)
		self.assertGreaterEqual(result[1][2], 0)


	def test__round_matrix_to_int__noop(self):
		result = round_matrix_to_int(TEST_MAT)
		for y in range(3):
			for x in range(3):
				self.assertEqual(result[y][x], TEST_MAT[y][x])


	def test__round_matrix_to_int_simple(self):
		result = round_matrix_to_int(TEST_FLOAT_MAT)
		self.assertEqual(result[0][0], 0)
		self.assertEqual(result[0][1], 1)
		self.assertEqual(result[0][2], 0)
		self.assertEqual(result[1][0], 0)
		self.assertEqual(result[1][1], 1)
		self.assertEqual(result[1][2], 0)
		self.assertEqual(result[2][0], 0)
		self.assertEqual(result[2][1], 1)
		self.assertEqual(result[2][2], 0)



if __name__ == "__main__":
	unittest.main()
