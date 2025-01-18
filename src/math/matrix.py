"""
Utility functions for smoothing matrixes out.
"""

from src.math.adj import adj_cells

def smooth_matrix(
	matrix,
	weight = 0.5,
	loop_x = True,
	loop_y = False,
	diag = True
):
	"""
	Smooths a matrix out.

	The weight is how much the tile should be affected by its neighbors. A
	weight of 0 will result in nothing, but a weight of 1 will make
	smoothed[y][x] the average of matrix[y][x] and everything adjacent to
	it.

	Use loop_x, loop_y, and diag to help determine which cells are adjacent.
	On a planet, we loop_x but do not loop_y. Recommended to use diag=True,
	but =False will produce a valid result too.
	"""
	h = len(matrix)
	w = len(matrix[0])

	smoothed = [[0] * w for _ in range(h)]

	for y in range(h):
		for x in range(w):
			v = matrix[y][x]
			sv = 1
			adj = adj_cells((w,h), (x,y), loop_x=loop_x, loop_y=loop_y, diag=diag)
			sv += len(adj) * weight
			for x2,y2 in adj:
				v += matrix[y2][x2] * weight
			smoothed[y][x] = v / sv

	return smoothed


def round_matrix_to_int(matrix):
	"""
	Rounds a matrix to integers.
	"""
	return [[int(round(v)) for v in row] for row in matrix]
