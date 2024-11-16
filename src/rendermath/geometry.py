"""
Functions for general geometry stuff. 
"""

from src.math.vector2 import vector2_average

def sign(o, a, b):
	"""
	TODO(jm) - WTF is this?!?!
	"""
	return (o[0] - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (o[1] - b[1])

def is_point_in_triangle(p, triangle):
	"""
	Given a point on the screen and a triangle in space (represented as an
	array of three points), return True if the point is inside the triangle.
	Points on edges count.
	"""
	v1, v2, v3 = triangle
	d1 = sign(p, v1, v2)
	d2 = sign(p, v2, v3)
	d3 = sign(p, v3, v1)
	has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
	has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
	return not (has_neg and has_pos)

def is_point_in_hexagon(p, hexagon):
	"""
	Is the point in a hexagon?
	"""
	center = vector2_average(hexagon)
	for i in range(6):
		j = (i + 1) % 6
		if is_point_in_triangle(p, (hexagon[i], hexagon[j], center)):
			return True
	return False

def is_point_in_rect(p, rect):
	"""
	Returns true if a point is inside a rectangle.
	"""
	x, y = p
	origin, dimensions = rect
	ox, oy = origin
	width, height = dimensions
	in_x = ox <= x < (ox + width)
	in_y = oy <= y < (oy + height)
	return in_x and in_y

def is_point_in_screen(p, dimensions):
	"""
	Wrapper for is_point_in_rect, screens don't have origins.
	"""
	return is_point_in_rect(p, ((0,0), dimensions))
