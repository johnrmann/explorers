"""
Functions for dealing with translating between cell space and screen space.

Note on naming - a "cell" is a position in the world grid. A cell's position
on the screen does not account for height. A tile's position on the screen
does.

Cells and tiles have the same dimension, but for the most part, are not the
same thing.
"""

from functools import cache

from src.math.direction import Direction
from src.rendermath.tile import tile_polygon

@cache
def cell_to_screen_transform(cell_pos, orientation: Direction):
	"""
	Transforms from cell space to screen space (screen space is diagonal
	isometric). Apply tile dimensions to get final coordinates.
	"""
	x, y = cell_pos
	if orientation == Direction.NORTHWEST:
		return (x - y, x + y)
	elif orientation == Direction.NORTHEAST:
		return (x + y, y - x)
	elif orientation == Direction.SOUTHEAST:
		return (y - x, -(x + y))
	elif orientation == Direction.SOUTHWEST:
		return (-(x + y), -(y - x))
	raise ArithmeticError("Unsupported orientation.")

def cell_position_on_global_screen(cell_pos, camera_dir, tile_dims):
	"""
	Return the pixel position of the cell on an infinite screen where the
	world origin is at screen position (0, 0).
	"""
	tile_width, tile_height = tile_dims
	half_w = tile_width // 2
	half_h = tile_height // 2
	tx, ty = cell_to_screen_transform(cell_pos, camera_dir)
	screen_x = tx * half_w
	screen_y = ty * half_h
	return (screen_x, screen_y)

def cell_polygon_on_global_screen(cell_pos, camera_dir, tile_dims):
	"""
	Given a cell position (in world space), camera direction, and the width and
	height of the tile, returns the coordinates of the cell's polygon as it
	would appear on an infite screen. World position of (0, 0) corresponds to
	infinite screen position of (0, 0).
	"""
	screen_pos = cell_position_on_global_screen(cell_pos, camera_dir, tile_dims)
	return tile_polygon(screen_pos, tile_dims)
