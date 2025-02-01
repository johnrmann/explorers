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
	"""
	Returns a copy of the given color such that each channel is multiplied by
	the given factor.
	"""
	if len(color) == 4:
		r,g,b,a = color
		return (round(k * r), round(k * g), round(k * b), a)
	elif len(color) == 3:
		r,g,b = color
		return (round(k * r), round(k * g), round(k * b))
	else:
		raise ValueError("Color must be a 3-tuple or 4-tuple.")


def average_color(color1, color2):
	"""
	Take the average of two colors.
	"""
	pairs = zip(color1, color2)
	return tuple((a + b) // 2 for a, b in pairs)


def alpha_mask_from_surface(surface, fill_color=None):
	"""
	Returns a copy of the given surface such that all non-transparent pixels
	are the given color (default opaque white).
	"""
	if fill_color is None:
		fill_color = (255, 255, 255, 255)
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


def resize_surface(surface, factor=1):
	"""
	Returns a copy of the given surface resized to the given dimensions.
	"""
	w, h = surface.get_size()
	w2 = int(round(w * factor))
	h2 = int(round(h * factor))
	return pygame.transform.scale(surface, (w2, h2))


def tint_surface(surface, color, intensity: float = 1):
	"""
	Tints the given image with the given color and intensity.
	"""

	r, g, b = color
	r2, g2, b2 = [round(c * intensity) for c in (r, g, b)]
	r2, g2, b2 = [max(0, min(255, c)) for c in (r2, g2, b2)]
	color2 = (r2, g2, b2)

	surf2 = surface.copy().convert_alpha()
	blend_surface = pygame.Surface(surface.get_size())
	blend_surface.fill(color2)
	surf2.blit(blend_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
	return surf2


def relight_surface(surface, factor=1):
	"""
	Returns a copy of the given surface such that each pixel color is
	multiplied by the given factor.
	"""
	return tint_surface(surface, (255, 255, 255), factor)
