"""
Utility functions for smoothing matrixes out.
"""

import math

from src.math.adj import adj_cells

def matrix_sized_as(
		matrix: list[list[int]],
		default: int = 0
) -> list[list[int]]:
	"""
	Returns a matrix of the same size as the given matrix, filled with the
	given default value.
	"""
	return [
		[default for _ in row]
		for row in matrix
	]


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


def matrix_double_width(matrix):
	"""
	Doubles a matrix's width, copying each cell over by the width of the
	matrix.
	"""
	h = len(matrix)
	w = len(matrix[0])
	new_matrix = [[0] * (w * 2) for _ in range(h)]
	for y in range(h):
		for x in range(w):
			new_matrix[y][x] = matrix[y][x]
			new_matrix[y][w + x] = matrix[y][x]
	return new_matrix


def matrix_minfold_width(matrix):
	"""
	Folds a matrix in half along the x-axis, taking the minimum value of
	each pair of cells.
	"""
	h = len(matrix)
	w = len(matrix[0])
	new_matrix = [[0] * (w // 2) for _ in range(h)]
	for y in range(h):
		for x in range(w // 2):
			new_matrix[y][x] = min(matrix[y][x], matrix[y][x + w // 2])
	return new_matrix


def _distances_to_nonzero_values(matrix: list[list[int]]):
	"""Helper for distances_to_nonzero_values."""
	width = len(matrix[0])
	height = len(matrix)

	seen = matrix_sized_as(matrix, default=math.inf)

	for y in range(height):
		for x in range(width):
			if matrix[y][x] != 0:
				seen[y][x] = 0
			else:
				if x > 0:
					seen[y][x] = min(seen[y][x], seen[y][x - 1] + 1)
				if y > 0:
					seen[y][x] = min(seen[y][x], seen[y - 1][x] + 1)

	for y in range(height - 1, -1, -1):
		for x in range(width - 1, -1, -1):
			if matrix[y][x] != 0:
				seen[y][x] = 0
			else:
				if x < width - 1:
					seen[y][x] = min(seen[y][x], seen[y][x + 1] + 1)
				if y < height - 1:
					seen[y][x] = min(seen[y][x], seen[y + 1][x] + 1)

	return seen


def distances_to_nonzero_values(
		matrix: list[list[int]],
		loop_x = True,
):
	"""
	Cells in matrix that are nonzero will be replaced with zero, and zero
	cells will be replaced by the distance to the nearest nonzero cell in the
	original matrix.
	"""
	if not loop_x:
		return _distances_to_nonzero_values(matrix)
	else:
		doubled = matrix_double_width(matrix)
		distances = _distances_to_nonzero_values(doubled)
		return matrix_minfold_width(distances)
