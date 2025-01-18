import unittest

from src.math.adj import adj_cells
from src.math.matrix import (
	matrix_sized_as,
	smooth_matrix,
	round_matrix_to_int,
	matrix_double_width,
	matrix_minfold_width,
	distances_to_nonzero_values,
)

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
	def test__matrix_sized_as__basic(self):
		result = matrix_sized_as(TEST_MAT, default=0)
		self.assertEqual(len(result), 3)
		self.assertEqual(len(result[0]), 3)
		for y in range(3):
			for x in range(3):
				self.assertEqual(result[y][x], 0)


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


	def test__matrix_double_width__basic(self):
		result = matrix_double_width(TEST_MAT)
		for y in range(3):
			for x in range(3):
				self.assertEqual(result[y][x], TEST_MAT[y][x])
				self.assertEqual(result[y][x + 3], TEST_MAT[y][x])


	def test__matrix_minfold_width__basic(self):
		test = [
			[0, 9, 0, 9, 0, 9],
			[9, 0, 9, 0, 9, 0],
			[0, 9, 0, 9, 0, 9],
		]
		result = matrix_minfold_width(test)
		self.assertEqual(len(result), 3)
		self.assertEqual(len(result[0]), 3)
		for y in range(3):
			for x in range(3):
				self.assertEqual(result[y][x], 0)


	def test__distances_to_nonzero_values__basic(self):
		oasis = [
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
		]
		expected = [
			[4, 3, 2, 3, 4],
			[3, 2, 1, 2, 3],
			[2, 1, 0, 1, 2],
			[3, 2, 1, 2, 3],
			[4, 3, 2, 3, 4],
		]
		result = distances_to_nonzero_values(oasis)
		self.assertEqual(result, expected)


	def test__distances_to_nonzero_values__edge_unlooped(self):
		oasis = [
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
		]
		expected = [
			[2, 3, 4, 5, 6],
			[1, 2, 3, 4, 5],
			[0, 1, 2, 3, 4],
			[1, 2, 3, 4, 5],
			[2, 3, 4, 5, 6],
		]
		result = distances_to_nonzero_values(oasis, loop_x=False)
		self.assertEqual(result, expected)


	def test__distances_to_nonzero_values__edge_looped(self):
		oasis = [
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[1, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0],
		]
		expected = [
			[2, 3, 4, 4, 3],
			[1, 2, 3, 3, 2],
			[0, 1, 2, 2, 1],
			[1, 2, 3, 3, 2],
			[2, 3, 4, 4, 3],
		]
		result = distances_to_nonzero_values(oasis, loop_x=True)
		self.assertEqual(result, expected)


if __name__ == "__main__":
	unittest.main()
