"""
Classes and functions for 2D vectors.
"""

from math import sqrt

class Vector2:
	"""
	A two-dimensional vector can either represent a direction or a point
	in two-dimensional space.
	"""

	__slots__ = ["x", "y"]

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __iter__(self):
		yield self.x
		yield self.y

	def __str__(self):
		return "({x:.2f}, {y:.2f})".format(x = self.x, y = self.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, q):
		qx, qy = q
		return self.x == qx and self.y == qy

	def __add__(self, q):
		qx, qy = q
		return Vector2(self.x + qx, self.y + qy)

	def __sub__(self, q):
		qx, qy = q
		return Vector2(self.x - qx, self.y - qy)

	def __mul__(self, k: float):
		return Vector2(self.x * k, self.y * k)

	def __div__(self, k: float):
		return Vector2(self.x / k, self.y / k)

	def __lt__(self, q):
		px,py = self
		qx,qy = q
		return (px,py) < (qx,qy)

	def __gt__(self,q):
		px,py = self
		qx,qy = q
		return (px,py) > (qx,qy)

	def is_cardinal(self):
		"""
		A vector represents a cardinal direction if either its x xor y
		coordinate is zero.
		"""
		if self.x == self.y == 0:
			return False
		return self.x == 0 or self.y == 0

	def is_diagonal(self):
		"""
		A direction is diagonal if its components are of the same magnitude.
		"""
		abs_x = abs(self.x)
		abs_y = abs(self.y)
		if abs_x == abs_y == 0:
			return False
		return abs_x == abs_y

	def magnitude2(self):
		"""
		Returns the square of the magnitude of the vector. For comparison
		operations, strongly prefer this over magnitude.
		"""
		x2 = self.x**2
		y2 = self.y**2
		return x2 + y2

	def magnitude(self):
		"""
		Returns the magnitude of the vector.
		"""
		return sqrt(self.magnitude2())

	def normalized(self):
		"""
		Returns a vector in the same direction such that the magnitude is 1.
		"""
		mag = self.magnitude()
		return Vector2(self.x / mag, self.y / mag)

	def round(self):
		"""Rounds the components of this vector to the nearest integer."""
		return Vector2(round(self.x), round(self.y))

def vector2_lerp(p: Vector2, q: Vector2, k: float) -> Vector2:
	"""
	Linearly interpolates between two vectors.
	"""
	dq = q - p
	return p + (dq * k)

def vector2_bounding_rect(ps):
	"""
	Returns the (origin, dimensions) of the smallest rect that fits all given
	points.
	"""
	if len(ps) == 0:
		raise ValueError('Need non-empty list')
	min_x = float('inf')
	max_x = -min_x
	min_y = float('inf')
	max_y = -min_y
	for p in ps:
		x, y = p
		min_x = min(x, min_x)
		min_y = min(y, min_y)
		max_x = max(x, max_x)
		max_y = max(y, max_y)
	origin = (min_x, min_y)
	dimensions = (max_x - min_x, max_y - min_y)
	return (origin, dimensions)

def vector2_move_points_near_zero(ps):
	"""
	Moves the given points close to the origin. For example...

		(1,1), (2,2) --> (0,0), (1,1)
		(0,1), (1,0) --> (0,1), (1,0)
	"""
	if len(ps) == 0:
		raise ValueError('Need non-empty list')
	min_x = float('inf')
	min_y = float('inf')
	for p in ps:
		x, y = p
		min_x = min(x, min_x)
		min_y = min(y, min_y)
	qs = []
	for p in ps:
		x, y = p
		qx = x - min_x
		qy = y - min_y
		qs.append((qx, qy))
	return qs

def vector2_average(ps):
	"""
	Computes the average of points.
	"""
	xs = [x for x, _ in ps]
	ys = [y for _, y in ps]
	return (
		sum(xs) / len(ps),
		sum(ys) / len(ps)
	)

def vector2_rotate_point(p, quarter_turns=0):
	"""
	Rotates a point by clockwise quarter turns.
	"""
	if quarter_turns >= 4:
		return vector2_rotate_point(p, quarter_turns=quarter_turns % 4)
	x, y = p
	if quarter_turns == 1:
		return (y, -x)
	elif quarter_turns == 2:
		return (-x, -y)
	elif quarter_turns == 3:
		return (-y, x)
	return p

def vector2_rotate_points(ps, quarter_turns=0):
	"""
	Rotates points by clockwise quarter turns.
	"""
	if quarter_turns >= 4:
		return vector2_rotate_points(ps, quarter_turns=quarter_turns % 4)
	if quarter_turns == 1:
		return [(y, -x) for x, y in ps]
	elif quarter_turns == 2:
		return [(-x, -y) for x, y in ps]
	elif quarter_turns == 3:
		return [(-y, x) for x, y in ps]
	return ps
