import pygame

from src.gui.gui import GuiElement

RED = (250, 0, 0)
GREEN = (0, 250, 0)

HEALTH_LAYERS = [
	(RED, 0, 0),
	(GREEN, 0, 100),
]

class Rangebar(GuiElement):
	"""
	A GUI Element rendering a bar with multiple layers.
	"""

	def __init__(self, rect=None, layers=None, values=None, parent=None):
		if rect is None:
			raise ValueError('Need rect.')
		if layers is None:
			layers = HEALTH_LAYERS
		upper_layers = layers[1:]
		if values is None:
			values = [(low + hi) // 2 for _, low, hi in upper_layers]
		origin, dimensions = rect
		self.relative_origin = origin
		self.dimensions = dimensions
		super().__init__(parent=parent)
		self.layers = layers
		self.values = values

	def _draw_background(self, screen):
		bg_color, __, __ = self.layers[0]
		pygame.draw.rect(screen, bg_color, self.pygame_rect)

	def _draw_layers(self, screen):
		w, h = self.dimensions
		x, y = self.origin
		for i in range(1, len(self.layers)):
			color, low, hi = self.layers[i]
			v = self.values[i - 1]
			diff = hi - low
			norm = v - low
			f = norm / diff
			draw_w = f * w
			pygame.draw.rect(screen, color, pygame.Rect(x, y, draw_w, h))

	def draw(self, screen):
		self._draw_background(screen)
		self._draw_layers(screen)
