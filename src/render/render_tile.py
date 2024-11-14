import pygame

from src.math.line import extrude_line_segment_y
from src.math.vector2 import (
	vector2_bounding_rect,
	vector2_move_points_near_zero
)
from src.rendermath.terrain import terrain_step_z_for_tile_width
from src.rendermath.tile import tile_polygon
from src.render.viewport import ZOOMS

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

GEN_HEIGHTS = 8

def _wall_for_direction_height_zoom(direction, z, zoom):
	tile_w = zoom
	tile_h = tile_w // 2
	tile = tile_polygon((tile_w // 2, tile_h // 2), (tile_w, tile_h))
	lineseg = (tile[1], tile[2])
	if direction == 'left':
		lineseg = (tile[2], tile[3])
	tile_z = terrain_step_z_for_tile_width(tile_w) * z
	return extrude_line_segment_y(lineseg, tile_z)

def _wall_surface(direction, h, zoom, color):
	wall = _wall_for_direction_height_zoom(direction, h, zoom)
	zeroed = vector2_move_points_near_zero(wall)
	__, (w,h) = vector2_bounding_rect(zeroed)
	surface = pygame.Surface((w,h), pygame.SRCALPHA)
	pygame.draw.polygon(surface, color, zeroed)
	return surface

class TileSurfaceCache:
	"""
	Pre-render diagonal tiles and their walls at different zooms and heights
	for faster rendering.
	"""

	tile_cache = {}
	left_wall_cache = {}
	right_wall_cache = {}

	zooms: list[int]

	def __init__(self, zooms=None):
		if zooms is None:
			zooms = ZOOMS
		self.zooms = zooms
		self._init_tile_cache()
		self._init_wall_caches()

	def _init_tile_cache(self):
		for zoom in self.zooms:
			w = zoom
			h = w // 2
			surface = pygame.Surface((w, h), pygame.SRCALPHA)
			tile = tile_polygon((w // 2, h // 2), (w, h))
			pygame.draw.polygon(surface, GROUND_COLOR, tile)
			self.tile_cache[zoom] = surface

	def _init_wall_caches(self):
		for zoom in self.zooms:
			self.left_wall_cache[zoom] = [None]
			self.right_wall_cache[zoom] = [None]
			for i in range(GEN_HEIGHTS):
				h = i + 1
				self.left_wall_cache[zoom].append(
					_wall_surface('left', h, zoom, WALL_COLOR_1)
				)
				self.right_wall_cache[zoom].append(
					_wall_surface('right', h, zoom, WALL_COLOR_2)
				)

	def tile_surface(self, zoom):
		"""
		Returns a pre-rendered tile top for the given zoom (tile width).
		"""
		return self.tile_cache[int(zoom)]

	def left_wall_surface(self, zoom, left_wall_h=0):
		"""
		Returns a pre-rendered left wall for the given zoom (tile width) and
		height. If the height is zero, return none.
		"""
		if left_wall_h != 0:
			left_wall_h = int(left_wall_h + 1)
			return self.left_wall_cache[zoom][left_wall_h]
		else:
			return None

	def right_wall_surface(self, zoom, right_wall_h=0):
		"""
		Returns a pre-rendered right wall for the given zoom (tile width) and
		height. If the height is zero, return none.
		"""
		if right_wall_h != 0:
			right_wall_h = int(right_wall_h + 1)
			return self.right_wall_cache[zoom][right_wall_h]
		else:
			return None

	def tile_surface_and_position(self, screen_p, zoom):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw and the zoom factor, return the tile surface and blit position
		(top left corner).
		"""
		surface = self.tile_surface(zoom)
		position = tile_screen_draw_position(screen_p, zoom)
		return surface, position

	def left_wall_surface_and_position(self, screen_p, zoom, wall_h=0):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw, the zoom factor, and the wall height, return the left wall
		surface and blit position (top left corner).
		"""
		surface = self.left_wall_surface(zoom, wall_h)
		if surface is None:
			return None
		position = left_wall_screen_draw_position(screen_p, zoom)
		return surface, position

	def right_wall_surface_and_position(self, screen_p, zoom, wall_h=0):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw, the zoom factor, and the wall height, return the right wall
		surface and blit position (top left corner).
		"""
		surface = self.right_wall_surface(zoom, wall_h)
		if surface is None:
			return None
		position = right_wall_screen_draw_position(screen_p, zoom)
		return surface, position

	def surfaces_and_positions(self, screen_p, zoom, wall_heights=None):
		"""
		Return the surfaces and draw positions (top left corners) for the
		(tile, left wall, right wall).
		"""
		if wall_heights is None:
			wall_heights = (0, 0)
		left, right = wall_heights
		return [
			self.tile_surface_and_position(screen_p, zoom),
			self.left_wall_surface_and_position(screen_p, zoom, wall_h=left),
			self.right_wall_surface_and_position(screen_p, zoom, wall_h=right)
		]

def tile_screen_draw_position(screen_p, tile_w):
	"""
	Given a center screen position and a tile width, return the top-left screen
	point of the tile for surface drawing.
	"""
	x, y = screen_p
	tile_h = tile_w // 2
	return (x - (tile_w // 2), y - (tile_h // 2))

def left_wall_screen_draw_position(screen_p, tile_w):
	"""
	Given a center tile screen position and a tile width, return the top-left
	screen point of the left wall for surface drawing.
	"""
	x, y = screen_p
	return (x - (tile_w // 2), y)

def right_wall_screen_draw_position(screen_p, __):
	"""
	How convenient, the right wall's top-left position is the tile's center
	position. We still define this function for clarity, though.
	"""
	return screen_p
