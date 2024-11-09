"""
A tile is an isometric tile on the screen. It is represented as four lines
between four points, in clockwise order: top, right, bottom, left.
"""

from src.rendermath.geometry import is_point_in_triangle

def tile_polygon(p, tile_dims, n=1):
	"""
	Returns a n x n tile centered at the screen position p.
	"""
	tile_width, tile_height = tile_dims
	h = (tile_height // 2) * n
	w = (tile_width // 2) * n
	x, y = p
	return [
		(x, y - h),
		(x + w, y),
		(x, y + h),
		(x - w, y)
	]

def is_point_in_tile(p, tile):
	"""
	Given a point on the screen and a tile (returned from tile_polygon),
	return True if the point is inside the tile. Points on edges count.
	"""
	top, right, bottom, left = tile
	l_half = (top, bottom, left)
	r_half = (top, bottom, right)
	return is_point_in_triangle(p, l_half) or is_point_in_triangle(p, r_half)
