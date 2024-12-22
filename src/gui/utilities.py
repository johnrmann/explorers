"""
These functions may be useful throughout the GUI module.
"""

import pygame

from src.rendermath.color import ensure_rgba

from src.gui.gui import GuiElement

def create_gradient_surface(height, start_color, end_color):
	"""
	Create a 1-pixel wide vertical gradient surface.
	"""

	surface = pygame.Surface((1, height), pygame.SRCALPHA)
	start_color = ensure_rgba(start_color)
	end_color = ensure_rgba(end_color)
	r1, g1, b1, a1 = start_color
	r2, g2, b2, a2 = end_color

	dr = r2 - r1
	dg = g2 - g1
	db = b2 - b1
	da = a2 - a1

	# Generate gradient colors
	for y in range(0, height - 1):
		ratio = y / (height - 1)
		r = int(r1 + dr * ratio)
		g = int(g1 + dg * ratio)
		b = int(b1 + db * ratio)
		a = int(a1 + da * ratio)
		surface.set_at((0, y), (r, g, b, a))
	surface.set_at((0, height - 1), end_color)

	return surface

def bounding_box(gui_elems: list[GuiElement]):
	"""
	Returns the bounding box that contains all GUI elements.
	"""
	if not gui_elems:
		return (0, 0), (0, 0)
	x1s = [elem.origin[0] for elem in gui_elems]
	y1s = [elem.origin[1] for elem in gui_elems]
	x2s = [elem.origin[0] + elem.dimensions[0] for elem in gui_elems]
	y2s = [elem.origin[1] + elem.dimensions[1] for elem in gui_elems]
	x1 = min(x1s)
	y1 = min(y1s)
	x2 = max(x2s)
	y2 = max(y2s)
	width = x2 - x1
	height = y2 - y1
	return (x1, y1), (width, height)
