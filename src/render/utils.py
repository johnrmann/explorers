import pygame

from src.render.viewport import Viewport

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

def alpha_mask_from_surface(surface, fill_color=(255, 255, 255, 255)):
	"""
	Returns a copy of the given surface such that all non-transparent pixels
	are the given color (default opaque white).
	"""
	if len(fill_color) != 4:
		raise ValueError("Fill color must be a 4-tuple.")
	if fill_color[3] != 255:
		raise ValueError("Fill color must be opaque.")
	alpha_mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
	alpha_mask.fill((0, 0, 0, 0))
	for x in range(surface.get_width()):
		for y in range(surface.get_height()):
			_, _, _, a = surface.get_at((x, y))
			if a == 0:
				continue
			alpha_mask.set_at((x, y), fill_color)
	return alpha_mask.convert_alpha()
