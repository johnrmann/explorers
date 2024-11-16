"""
Classes and functions for 3D vectors.
"""

from src.math.vector2 import vector2_rotate_point

class Vector3:
	"""
	A 3-dimensional vector can represent either a direction or point in 3d
	space.
	"""

	__slots__ = ["x", "y", "z"]

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z

	def __eq__(self, q):
		qx, qy, qz = q
		return (self.x == qx) and (self.y == qy) and (self.z == qz)

def vector3_rotate_point(p, quarter_turns=0):
	"""
	Rotates a point by clockwise quarter turns.
	"""
	x, y, z = p
	nx, ny = vector2_rotate_point((x, y), quarter_turns=quarter_turns)
	return Vector3(nx, ny, z)

def vector3_rotate_points(ps, quarter_turns=0):
	"""
	Rotates points by clockwise quarter turns.
	"""
	for x, y, z in ps:
		nx, ny = vector2_rotate_point((x, y), quarter_turns=quarter_turns)
		yield Vector3(nx, ny, z)
