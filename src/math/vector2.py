"""
TODO(jm)
"""

from math import sqrt

class Vector2:
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
		abs_x = abs(self.x)
		abs_y = abs(self.y)
		if abs_x == abs_y == 0:
			return False
		return abs_x == abs_y
	
	def magnitude2(self):
		x2 = self.x**2
		y2 = self.y**2
		return x2 + y2
	
	def magnitude(self):
		return sqrt(self.magnitude2())
	
	def normalized(self):
		mag = self.magnitude()
		return Vector2(self.x / mag, self.y / mag)

	def round(self):
		"""Rounds the components of this vector to the nearest integer."""
		return Vector2(round(self.x), round(self.y))

def vector2_lerp(p: Vector2, q: Vector2, k: float) -> Vector2:
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
