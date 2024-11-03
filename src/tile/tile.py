"""
A tile is an isometric tile on the screen. It is represented as four lines
between four points, in clockwise order: top, right, bottom, left.
"""

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
