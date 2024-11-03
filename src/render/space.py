"""
Functions for transforming between tile space and screen space.
"""

from src.math.direction import Direction
from src.render.viewport import Viewport

def _tile_screen_transform(p, orientation: Direction):
	x, y = p
	if orientation == Direction.NORTHWEST:
		return (x - y, x + y)
	elif orientation == Direction.NORTHEAST:
		return (x + y, y - x)
	elif orientation == Direction.SOUTHEAST:
		return (y - x, -(x + y))
	elif orientation == Direction.SOUTHWEST:
		return (-(x + y), -(y - x))
	raise ArithmeticError("Unsupported orientation.")

def _global_tile_to_screen_coords(p, vp: Viewport):
	half_w = vp.tile_width // 2
	half_h = vp.tile_height // 2
	tx, ty = _tile_screen_transform(p, vp.camera_orientation)
	screen_x = tx * half_w
	screen_y = ty * half_h
	return (screen_x, screen_y)

def tile_to_screen_coords(p_tile, vp: Viewport):
	"""
	Converts tile coordinates to screen coordinates.
	"""
	win_width, win_height = vp.window_dims
	cx_screen, cy_screen = _global_tile_to_screen_coords(vp.camera_pos, vp)
	x2,y2 = _global_tile_to_screen_coords(p_tile, vp)
	return (
		x2 + (win_width // 2) - cx_screen,
		y2 + (win_height // 2) - cy_screen,
	)

def screen_to_tile_coords(p_screen, vp):
	"""
	Converts screen coordinates back into tile coordinates, considering camera
	orientation.
	"""
	# Center the camera in screen coordinates
	screen_x, screen_y = p_screen
	win_width, win_height = vp.window_dims
	cx_screen, cy_screen = _global_tile_to_screen_coords(vp.camera_pos, vp)
	
	# Adjust the screen coordinates relative to the centered camera
	rel_screen_x = screen_x - (win_width // 2) + cx_screen
	rel_screen_y = screen_y - (win_height // 2) + cy_screen

	# Precompute half tile width and height
	half_tw = vp.tile_width // 2
	half_th = vp.tile_height // 2
	
	# Apply the reverse transformation based on camera orientation
	if vp.camera_orientation == Direction.NORTHWEST:
		# Default orientation
		x = (rel_screen_x // half_tw + rel_screen_y // half_th) // 2
		y = (rel_screen_y // half_th - rel_screen_x // half_tw) // 2
	elif vp.camera_orientation == Direction.NORTHEAST:
		# 90-degree clockwise rotation
		x = (rel_screen_y // half_th - rel_screen_x // half_tw) // 2
		y = (rel_screen_y // half_th + rel_screen_x // half_tw) // 2
	elif vp.camera_orientation == Direction.SOUTHEAST:
		# 180-degree rotation
		x = -(rel_screen_x // half_tw + rel_screen_y // half_th) // 2
		y = -(rel_screen_y // half_th - rel_screen_x // half_tw) // 2
	elif vp.camera_orientation == Direction.SOUTHWEST:
		# 90-degree counterclockwise rotation
		x = (rel_screen_x // half_tw - rel_screen_y // half_th) // 2
		y = -(rel_screen_x // half_tw + rel_screen_y // half_th) // 2
	else:
		raise ValueError("Unsupported camera orientation")

	return (x, y)
