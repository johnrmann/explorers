import math

from src.math.point import point_plus

def distance2(p, q):
	"""
	Squared distance between two points. Strongly prefer using this over
	distance, as sqrt is expensive.
	"""
	x1, y1 = p
	x2, y2 = q
	dy = abs(y2 - y1)
	dx = abs(x2 - x1)
	return (dy * dy) + (dx * dx)

def distance(p, q):
	"""
	Euclid distance between two points.
	"""
	return math.sqrt(distance2(p, q))

def _advanced_manhattan_distance(
	p,
	q,
	d,
	loop_x = False,
	loop_y = False,
):
	w, h = d
	distances = [manhattan_distance(p, q)]
	if loop_x:
		q2 = point_plus(q, (w, 0))
		q3 = point_plus(q, (-w, 0))
		distances.append(manhattan_distance(p, q2))
		distances.append(manhattan_distance(p, q3))
	if loop_y:
		q2 = point_plus(q, (0, h))
		q3 = point_plus(q, (0, -h))
		distances.append(manhattan_distance(p, q2))
		distances.append(manhattan_distance(p, q3))
	return min(distances)

def manhattan_distance(p, q):
	"""
	Manhattan distance between two points.
	"""
	x1,y1 = p
	x2,y2 = q
	dx = abs(x1 - x2)
	dy = abs(y1 - y2)
	return dx + dy

def planet_distance2(p, q, d):
	"""
	On a planet, the x-axis is looped. Compute the distance between two
	points, keeping in mind that the shortest distance may be across the
	international dateline.

	p and q are the points, d = (w, h) is the size of the planet.
	"""
	w, h = d
	dist1 = distance2(p, q)
	x, y = p
	p2 = (x + w, y)
	dist2 = distance2(p2, q)
	a, b = q
	q2 = (a + w, y)
	dist3 = distance2(p, q2)
	return min(dist1, dist2, dist3)

def planet_manhattan_distance(p, q, d):
	"""
	On a planet, the x-axis is looped.
	"""
	return _advanced_manhattan_distance(p, q, d, loop_x=True)

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
