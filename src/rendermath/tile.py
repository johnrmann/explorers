"""
A tile is an isometric tile on the screen. It is represented as four lines
between four points, in clockwise order: top, right, bottom, left.
"""

from src.math.vector2 import Vector2

from src.rendermath.geometry import is_point_in_triangle

def tile_polygon(p, tile_dims, n=1):
	"""
	Returns a n x n tile centered at the screen position p.
	"""
	tile_w, tile_h = tile_dims
	h = (tile_h // 2) * n
	w = (tile_w // 2) * n
	x, y = p
	return [
		(x, y - h),
		(x + w, y),
		(x, y + h),
		(x - w, y)
	]

def tile_top_y(tile):
	"""Returns the top coordinate of the tile."""
	return tile[0][1]

def tile_right_x(tile):
	"""Returns the right coordinate of the tile."""
	return tile[1][0]

def tile_bottom_y(tile):
	"""Returns the bottom corrdinate of the tile."""
	return tile[2][1]

def tile_left_x(tile):
	"""Returns the left coordinate of the tile."""
	return tile[3][0]

def tile_width(tile):
	"""Returns the tile width."""
	return tile_right_x(tile) - tile_left_x(tile)

def tile_height(tile):
	"""Returns the tile height."""
	return tile_bottom_y(tile) - tile_top_y(tile)

def is_tile_in_rect(tile, rect: tuple[Vector2, Vector2]):
	"""
	Returns whether or not the tile is inside a rect.
	"""
	if not tile:
		return False
	origin, dimensions = rect
	ox, oy = origin
	width, height = dimensions
	too_high = tile_bottom_y(tile) < oy
	too_low = tile_top_y(tile) > oy + height
	too_left = tile_right_x(tile) < ox
	too_right = tile_left_x(tile) > ox + width
	return not (too_high or too_low or too_left or too_right)

def is_tile_in_screen(tile, dimensions: Vector2):
	"""
	Returns whether the tile is in a screen with the given dimensions.
	"""
	if not tile:
		return False
	return is_tile_in_rect(tile, (Vector2(0,0), dimensions))

def is_point_in_tile(p, tile):
	"""
	Given a point on the screen and a tile (returned from tile_polygon),
	return True if the point is inside the tile. Points on edges count.
	"""
	if not tile or not p:
		return False
	top, right, bottom, left = tile
	l_half = (top, bottom, left)
	r_half = (top, bottom, right)
	return is_point_in_triangle(p, l_half) or is_point_in_triangle(p, r_half)
