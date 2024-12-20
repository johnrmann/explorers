import pygame

from src.gui.gui import GuiElement

def is_2d_series(series):
	"""Returns True if the series is a list of 2D points."""
	if not series:
		raise ValueError("Series is empty.")
	if isinstance(series[0], (int, float)):
		return False
	return True

def series_x_range(series):
	"""
	Returns the (min, max) x values in the series. If given a series of 2D
	points, use the first coordinate. If given a series of values, use the
	array indexes.
	"""
	x_values = []
	if is_2d_series(series):
		x_values = [x for x, y in series]
		return min(x_values), max(x_values)
	else:
		return 0, len(series) - 1

def series_y_range(series):
	"""
	Returns the (min, max) y values in the series. If given a series of 2D
	points, use the second coordinate. If given a series of values, use the
	values.
	"""
	y_values = []
	if is_2d_series(series):
		y_values = [y for x, y in series]
	else:
		y_values = series
	return min(y_values), max(y_values)

def series_to_screen(draw_origin, draw_dims, series):
	"""Converts a series of points to screen coordinates."""
	origin_x, origin_y = draw_origin
	width, height = draw_dims
	end_y = origin_y + height
	min_x, max_x = series_x_range(series)
	min_y, max_y = series_y_range(series)
	x_range = max_x - min_x
	y_range = max_y - min_y
	x_scale = width / x_range
	y_scale = height / y_range
	xys = series
	if not is_2d_series(series):
		xys = [(i, y) for i, y in enumerate(series)]
	screen_series = [
		((x - min_x) * x_scale + origin_x, end_y - ((y - min_y) * y_scale))
		for x, y in xys
	]
	return screen_series

class LineGraph(GuiElement):
	"""
	Render a line graph of one or more series of points.
	"""

	def __init__(
		self,
		origin=None,
		dimensions=None,
		parent=None,
		series=None,
		colors=None,
	):
		super().__init__(origin=origin, dimensions=dimensions, parent=parent)
		self.series = series
		self.colors = colors
		self.background_color = (0, 0, 0)

	def _draw_background(self, surface):
		pygame.draw.rect(surface, self.background_color, self.pygame_rect)

	def _draw_points(self, surface, points, color):
		screen_points = series_to_screen(self.origin, self.dimensions, points)
		ps = screen_points[:-1]
		qs = screen_points[1:]
		for p, q in zip(ps, qs):
			pygame.draw.line(surface, color, p, q)

	def _draw(self, surface):
		self._draw_background(surface)
		for points, color in zip(self.series, self.colors):
			self._draw_points(surface, points, color)
