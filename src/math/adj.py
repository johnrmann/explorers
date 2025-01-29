"""
This module contains functions for working with the concept of adjacency,
including: (1) working with adjacency matrices, (2) determining whether
two cells are adjacent, and (3) finding cells that are a certain number of
steps away from a given cell.
"""

from collections import deque

from src.math.direction import (
	is_direction_diagonal,
	direction_to_delta,
	Direction
)
from src.math.vector2 import Vector2


def keyed_adj_cells(d, p, loop_x = True, loop_y = False, diag = False):
	"""
	Returns a dictionary of points such that result[direction] = the cell
	at that direction relative to p. If it's out of bounds, None will
	be there instead.

	Optional flags for loop_x/y indicate whether to perform logic modulo
	dimensions. On a planet, the x-axis is looped, but the y-axis isn't.

	Optional flag to consider diagonal cells in addition to cardinal ones.
	"""
	w, h = d
	x, y = p
	qs = {}
	for dcn in Direction:
		if not diag and is_direction_diagonal(dcn):
			continue
		dx, dy = direction_to_delta(dcn)
		x2 = x + dx
		y2 = y + dy
		if not loop_x and (x2 >= w or x2 < 0):
			continue
		if not loop_y and (y2 >= h or y2 < 0):
			continue
		x2 = x2 % w
		y2 = y2 % h
		qs[dcn] = Vector2(x2, y2)
	return qs


def adj_cells(d, p, loop_x = True, loop_y = False, diag = False):
	"""
	Returns an array of cells in a d = (w, h) matrix adjacent to p = (x, y).

	Optional flags for loop_x/y indicate whether to perform logic modulo
	dimensions. On a planet, the x-axis is looped, but the y-axis isn't.

	Optional flag to consider diagonal cells in addition to cardinal ones.
	"""
	return list(
		keyed_adj_cells(d, p, loop_x=loop_x, loop_y=loop_y, diag=diag).values()
	)


def bool_adj_from_labels(
		matrix,
		n_labels,
		loop_x = True,
		loop_y = False,
		diag = False
):
	"""
	Returns an adj matrix given a labeled matrix. loop_x, loop_y, and diag are
	passed to `adj_cells` - see documentation for that function.
	"""
	adj = [[False] * n_labels for i in range(n_labels)]
	w = len(matrix[0])
	h = len(matrix)
	d = (w, h)
	for y in range(h):
		for x in range(w):
			if x == y:
				continue
			p = (x, y)
			cells = adj_cells(d, p, loop_x=loop_x, loop_y=loop_y, diag=diag)
			for q in cells:
				a, b = q
				val_p = matrix[y][x]
				val_q = matrix[b][a]
				if val_p == val_q:
					continue
				adj[val_p][val_q] = True
				adj[val_q][val_p] = True
	return adj


def select_adj_degree(b_adj, p, degree=1):
	"""
	Given an adjacency matrix and starting point index p, returns
	a set of point indexes that are `degree` degrees removed from
	p or less.
	"""
	visited = set([p])
	queue = deque([(p, 0)])
	result = set()

	while queue:
		node, dist = queue.popleft()

		# If within the degree limit, add to result set
		if dist <= degree:
			result.add(node)

		# Stop if we have reached the max degree for this path
		if dist == degree:
			continue

		# Check neighbors
		for neighbor, connected in enumerate(b_adj[node]):
			if connected and neighbor not in visited:
				visited.add(neighbor)
				queue.append((neighbor, dist + 1))
	return result


def are_cells_adj_cardinally(p: Vector2, q: Vector2):
	"""
	Returns true if the two cells share an edge.
	"""
	if p.x == q.x:
		return abs(p.y - q.y) == 1
	elif p.y == q.y:
		return abs(p.x - q.x) == 1
	return False


def are_cells_adj_diagonally(p: Vector2, q: Vector2):
	"""
	Returns true if the two cells share a corner, but not an edge.
	"""
	return abs(p.x - q.x) == 1 and abs(p.y - q.y) == 1


def are_cells_adj(p: Vector2, q: Vector2):
	"""
	Returns true if the cells are adjacent.
	"""
	return are_cells_adj_cardinally(p, q) or are_cells_adj_diagonally(p, q)


def cells_n_steps_from_cell(
		origin: Vector2 = None,
		n_steps: int = None,
		dimensions: Vector2 = None,
		loop_x: bool = True,
		loop_y: bool = False,
):
	"""
	Returns those cells that are exactly n_steps cardinal steps away from the
	origin cell.
	"""
	if origin is None or n_steps is None or dimensions is None:
		raise ValueError("origin and n_steps must be provided.")

	if n_steps == 0:
		yield origin
		return

	ox, oy = origin
	for dx in range(-n_steps, n_steps + 1):
		for dy in range(-n_steps, n_steps + 1):
			if abs(dx) + abs(dy) != n_steps:
				continue
			x = ox + dx
			y = oy + dy
			if not loop_x and (x >= dimensions.x or x < 0):
				continue
			if not loop_y and (y >= dimensions.y or y < 0):
				continue
			x = x % dimensions.x
			y = y % dimensions.y
			yield Vector2(x, y)
