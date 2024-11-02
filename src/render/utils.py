from src.render.viewport import Viewport

def tile_coords_to_global_screen_coords(x, y, vp: Viewport):
	"""
	Returns the center coordinates of this tile on an infinite screen.
	"""
	screen_x = (x - y) * (vp.tile_width // 2)
	screen_y = (x + y) * (vp.tile_height // 2)
	return (screen_x, screen_y)

def tile_coords_to_screen_coords(tile, vp: Viewport):
	"""
	tile_x, tile_y = 0, 0 and camera_x, camera_y = 0, 0 -> 
	"""
	win_width, win_height = vp.window_dims
	x,y = tile
	cx,cy = vp.camera_pos
	cx_screen, cy_screen = tile_coords_to_global_screen_coords(cx,cy,vp)
	x2,y2 = tile_coords_to_global_screen_coords(x, y, vp)
	return (
		x2 + (win_width // 2) - cx_screen,
		y2 + (win_height // 2) - cy_screen,
	)

def tile_polygon(x, y, vp: Viewport):
	return [
		(x, y - vp.tile_height // 2),
		(x + vp.tile_width // 2, y),
		(x, y + vp.tile_height // 2),
		(x - vp.tile_width // 2, y)
	]

def height_offset_tile(tile, dh, vp: Viewport):
	"""
	Math weirdness - making a tile go up means going to the top of the screen
	means subtraction.
	"""
	return [(p[0], p[1] - dh * vp.tile_z) for p in tile]

def box_between_tiles(top, bottom):
	"""
	Given a top tile and a bottom tile, returns three sets of polygon coords
	representing the box defined by the two, in the following order: top,
	left, and right.
	"""
	return (
		top,
		[top[3], top[2], bottom[2], bottom[3]],
		[top[2], top[1], bottom[1], bottom[2]]
	)

def scale_color(color, k):
	r,g,b = color
	return (k * r, k * g, k * b)
