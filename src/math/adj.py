from collections import deque

from src.math.direction import *
from src.math.vector2 import Vector2

STEP = [-1, 0, 1]

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

def bool_adj_from_labels(matrix, n_labels, loop_x = True, loop_y = False, diag = False):
	"""
	Returns an adj matrix given a labeled matrix. loop_x, loop_y, and diag are passed
	to `adj_cells` - see documentation for that function.
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

