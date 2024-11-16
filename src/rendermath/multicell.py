"""
Functions for dealing with many cells at a time.
"""

from src.math.direction import Direction

from src.rendermath.cell import cell_position_on_global_screen

_MULTICELL_SCREEN_RADIX = {
	Direction.NORTHWEST: 0,
	Direction.NORTHEAST: 1,
	Direction.SOUTHEAST: 2,
	Direction.SOUTHWEST: 3
}

def multicell_screen_diamond_cells(bounds, cam_dir=Direction.NORTHWEST):
	"""
	A rectangular collection of cells appears to be a diamond when rendered in
	a diagonal isometric perspective.

	This function returns the (top, right, bottom, left) coordinates of the
	cells at those corners.
	"""
	p, q = bounds
	px, py = p
	qx, qy = q
	min_x = min(px, qx)
	min_y = min(py, qy)
	max_x = max(px, qx)
	max_y = max(py, qy)
	points = [
		(min_x, min_y),
		(max_x, min_y),
		(max_x, max_y),
		(min_x, max_y)
	]
	radix = _MULTICELL_SCREEN_RADIX[cam_dir]
	for i in range(radix, len(points)):
		yield points[i]
	for i in range(0, radix):
		yield points[i]

def multicell_screen_top(bounds, cam_dir=Direction.NORTHWEST):
	"""
	Returns the topmost cell on the screen within the given
	bounds=(cell1, cell2 = (x,y)).
	"""
	top, _, _, _ = multicell_screen_diamond_cells(bounds, cam_dir)
	return top

def multicell_screen_right(bounds, cam_dir=Direction.NORTHWEST):
	"""
	Returns the rightmost cell on the screen within the given
	bounds=(cell1, cell2 = (x,y)).
	"""
	_, right, _, _ = multicell_screen_diamond_cells(bounds, cam_dir)
	return right

def multicell_screen_left(bounds, cam_dir=Direction.NORTHWEST):
	"""
	Returns the leftmost cell on the screen within the given
	bounds=(cell1, cell2 = (x,y)).
	"""
	_, _, _, left = multicell_screen_diamond_cells(bounds, cam_dir)
	return left

def multicell_screen_bottom(bounds, cam_dir=Direction.NORTHWEST):
	"""
	Returns the bottommost cell on the screen within the given
	bounds=(cell1, cell2 = (x,y)).
	"""
	_, _, bottom, _ = multicell_screen_diamond_cells(bounds, cam_dir)
	return bottom

def multicell_polygon_on_global_screen(bounds, cam_dir: Direction, tile_dims):
	"""
	Returns the points of the multicell on an infinite screen.
	"""
	tile_w, tile_h = tile_dims
	dx = tile_w // 2
	dy = tile_h // 2
	top, right, bottom, left = multicell_screen_diamond_cells(bounds, cam_dir)
	tx, ty = cell_position_on_global_screen(top, cam_dir, tile_dims)
	rx, ry = cell_position_on_global_screen(right, cam_dir, tile_dims)
	bx, by = cell_position_on_global_screen(bottom, cam_dir, tile_dims)
	lx, ly = cell_position_on_global_screen(left, cam_dir, tile_dims)
	yield (tx, ty - dy)
	yield (rx + dx, ry)
	yield (bx, by + dy)
	yield (lx - dx, ly)
