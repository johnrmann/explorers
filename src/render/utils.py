import pygame

from src.render.viewport import Viewport

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

def stand_rect_on_tile(rect, tile):
	ratio = rect.width / rect.height
	tile_leftmost = tile[3][0]
	tile_rightmost = tile[1][0]
	tile_center_y = (tile[0][1] + tile[2][1]) / 2
	tile_width = tile_rightmost - tile_leftmost
	rect_height = tile_width / ratio
	return pygame.Rect(
		(tile_leftmost, tile_center_y - rect_height),
		(tile_width, rect_height)
	)