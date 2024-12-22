"""
Functions and classes for scanlines.
"""

import pygame

from src.gui.gui import GuiElement
from src.gui.utilities import bounding_box, create_gradient_surface

class Scanline(GuiElement):
	"""
	Renders an animated scanline over the child elements. Gives off an
	aesthetic of an old CRT or oscilloscope monitor. Pretty cool!
	"""

	pixels_per_second = 100
	draw_offset = 0
	scan_height = 64

	def __init__(self, start_color, end_color, scan_height=64, **kwargs):
		super().__init__(**kwargs)
		self.start_color = start_color
		self.end_color = end_color
		self.scanline_surface = None
		self.scanline_scaled = None
		self.scan_height = scan_height

	def _make_scanline_surface(self):
		self.scanline_surface = create_gradient_surface(
			self.scan_height, self.start_color, self.end_color
		)
		draw_dims = (self.dimensions[0], self.scan_height)
		self.scanline_scaled = pygame.transform.scale(
			self.scanline_surface, draw_dims
		)

	def add_child(self, child):
		super().add_child(child)
		_, dims = bounding_box(self.elements)
		self.dimensions = dims
		self._make_scanline_surface()

	def my_update(self, dt):
		if self.scanline_surface is None:
			return
		self.draw_offset += self.pixels_per_second * dt
		if self.draw_offset > self.dimensions[1]:
			self.draw_offset = -self.scan_height
		self.draw_offset = int(self.draw_offset)

	def my_after_draw(self, screen):
		if self.scanline_surface is None:
			return
		ox, oy = self.origin
		subsurface = pygame.Surface(self.dimensions, pygame.SRCALPHA)
		subsurface.blit(self.scanline_scaled, (0, self.draw_offset))
		screen.blit(subsurface, (ox, oy))
