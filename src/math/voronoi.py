import numpy as np
from scipy.spatial import cKDTree, Voronoi

from src.math.random import random_2d_integers_numpy

def make_voronoi(dimensions, density):
	"""
	Creates a voronoi matrix with dimensions = (width * height). The x-axis is
	looped, as is the case on a planet. The density is the average area of the
	voronoi regions. (width * height) / density points will be created.
	"""

	width, height = dimensions
	num_points = width * height // density

	rand_points = random_2d_integers_numpy(num_points, width, height)
	wrapped_points = np.vstack([
		rand_points,
		rand_points + [width, 0],
		rand_points - [width, 0],
	])

	y_indices, x_indices = np.indices((height, width))
	cell_coords = np.column_stack(
		(x_indices.ravel(), y_indices.ravel())
	)

	tree  = cKDTree(wrapped_points)
	_, regions = tree.query(cell_coords)
	regions = regions % num_points
	matrix = regions.reshape((height, width))

	py_matrix = [[0] * width for _ in range(height)]
	for y in range(height):
		for x in range(width):
			py_matrix[y][x] = matrix[y, x]

	return py_matrix
