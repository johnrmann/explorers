"""
Functions for computing distance.

Module convention: `p / q = (x, y)` are points, `d = (w, h)` is the dimensions
of the world.
"""

import math

from src.math.vector2 import Vector2

ROOT_2 = math.sqrt(2)
SIGNS = [-1, 0, 1]

def distance2(p, q) -> float:
	"""
	Squared distance between two points. Strongly prefer using this over
	distance, as sqrt is expensive.
	"""
	x1, y1 = p
	x2, y2 = q
	dy = abs(y2 - y1)
	dx = abs(x2 - x1)
	return (dy * dy) + (dx * dx)

def distance(p, q) -> float:
	"""
	Euclid distance between two points.
	"""
	return math.sqrt(distance2(p, q))

def looped_distance(
	fn,
	p: Vector2,
	q: Vector2,
	d: Vector2,
	loop_x = False,
	loop_y = False,
) -> float:
	"""
	Uses an arbitrary distance function fn to compute the best distance over
	a world that can be looped on the x- and/or y-axis.
	"""
	w, h = d
	distances = [fn(p, q)]
	sign_x = [0] if not loop_x else SIGNS
	sign_y = [0] if not loop_y else SIGNS
	for sx in sign_x:
		for sy in sign_y:
			q2 = Vector2(w * sx, h * sy) + q
			distances.append(fn(p, q2))
	return min(distances)

def manhattan_distance(p: Vector2, q: Vector2) -> float:
	"""
	Manhattan distance between two points.
	"""
	if not isinstance(p, Vector2):
		px,py = p
		p = Vector2(px,py)
	delta = p - q
	return abs(delta.x) + abs(delta.y)

def washington_distance(p: Vector2, q: Vector2) -> float:
	"""
	Washington distance is similar to the Manhattan distance, except we can
	move diagonally as well, saving some distance.
	
	(Naming background: the L'Enfant Plan for Wash. DC includes a cartesian
	grid and diagonal roads, whereas Manhattan is pure Cartesian.)
	"""
	dx, dy = q - p
	min_dim = abs(min(dx, dy))
	diff = abs(dx - dy)
	return (min_dim * ROOT_2) + diff

def planet_distance2(p, q, d):
	"""
	On a planet, the x-axis is looped. Compute the distance between two
	points, keeping in mind that the shortest distance may be across the
	international dateline.

	p and q are the points, d = (w, h) is the size of the planet.
	"""
	return looped_distance(distance2, p, q, d, loop_x=True)

def planet_manhattan_distance(p: Vector2, q: Vector2, d: Vector2):
	"""
	On a planet, the x-axis is looped.
	"""
	return looped_distance(manhattan_distance, p, q, d, loop_x=True)

def planet_washington_distance(p: Vector2, q: Vector2, d: Vector2):
	"""
	On a planet, the x-axis is looped.
	"""
	return looped_distance(washington_distance, p, q, d, loop_x=True)

def min_planet_distance2(p, qs, d):
	"""
	Like planet_distance2 but with a loop.
	"""
	min_dist = float('inf')
	result = None
	for q in qs:
		dist = planet_distance2(p, q, d)
		if dist < min_dist:
			result = q
			min_dist = dist
	return result
