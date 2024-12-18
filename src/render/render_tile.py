import pygame

from functools import lru_cache

from src.math.line import extrude_line_segment_y
from src.math.vector2 import (
	vector2_bounding_rect,
	vector2_move_points_near_zero
)
from src.rendermath.terrain import terrain_step_z_for_tile_width
from src.rendermath.tile import tile_polygon
from src.render.viewport import ZOOMS
from src.rendermath.tile import tile_z_for_width

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

GEN_HEIGHTS = 8

# Numeric codes for which ridges to draw. Faster than using a boolean tuple.
NO_RIDGES = 0
LEFT_RIDGE = 1
RIGHT_RIDGE = 2
BOTH_RIDGES = LEFT_RIDGE | RIGHT_RIDGE

def _wall_for_direction_height_zoom(direction, z, zoom):
	tile_w = zoom
	tile_h = tile_w // 2
	tile = tile_polygon((tile_w // 2, tile_h // 2), (tile_w, tile_h))
	lineseg = (tile[1], tile[2])
	if direction == 'left':
		lineseg = (tile[2], tile[3])
	tile_z = terrain_step_z_for_tile_width(tile_w) * z
	return extrude_line_segment_y(lineseg, tile_z)

class TileSurfaceCache:
	"""
	Pre-render diagonal tiles and their walls at different zooms and heights
	for faster rendering.
	"""

	tile_cache = {}

	left_ridge_cache = {}
	right_ridge_cache = {}
	both_ridge_cache = {}

	_jut = None

	zooms: list[int]

	def __init__(self, zooms=None):
		if zooms is None:
			zooms = ZOOMS
		self.zooms = zooms
		self._init_tile_cache()
		self._init_ridge_caches()
		self._init_jut()

	def _make_tile_and_surface(self, w):
		z = tile_z_for_width(w)
		h = (w // 2)
		surface = pygame.Surface((w, h + z), pygame.SRCALPHA).convert_alpha()
		tile = tile_polygon((w // 2, h // 2), (w, h))
		pygame.draw.polygon(surface, GROUND_COLOR, tile)

		# Now draw the tile's walls.
		left_wall = _wall_for_direction_height_zoom('left', 8, w)
		right_wall = _wall_for_direction_height_zoom('right', 8, w)
		pygame.draw.polygon(surface, WALL_COLOR_1, left_wall)
		pygame.draw.polygon(surface, WALL_COLOR_2, right_wall)

		return tile, surface

	def _init_tile_cache(self):
		for zoom in self.zooms:
			_, surface = self._make_tile_and_surface(zoom)
			self.tile_cache[zoom] = surface

	def _init_ridge_caches(self):
		for zoom in self.zooms:
			tile, both = self._make_tile_and_surface(zoom)
			_, left = self._make_tile_and_surface(zoom)
			_, right = self._make_tile_and_surface(zoom)
			tile_top, tile_right, _, tile_left = tile
			pygame.draw.line(left, WALL_COLOR_1, tile_left, tile_top)
			pygame.draw.line(both, WALL_COLOR_1, tile_left, tile_top)
			pygame.draw.line(right, WALL_COLOR_1, tile_top, tile_right)
			pygame.draw.line(both, WALL_COLOR_1, tile_top, tile_right)
			self.left_ridge_cache[zoom] = left
			self.right_ridge_cache[zoom] = right
			self.both_ridge_cache[zoom] = both

	def _init_jut(self):
		self._jut = {
			NO_RIDGES: self.tile_cache,
			LEFT_RIDGE: self.left_ridge_cache,
			RIGHT_RIDGE: self.right_ridge_cache,
			BOTH_RIDGES: self.both_ridge_cache
		}

	def tile_surface_and_position(self, screen_p, zoom, ridges=None):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw and the zoom factor, return the tile surface and blit position
		(top left corner).
		"""
		idx = int(zoom)
		if ridges is None:
			ridges = NO_RIDGES
		surface = self._jut[ridges][idx]
		position = tile_screen_draw_position(screen_p, zoom)
		return surface, position

def tile_screen_draw_position(screen_p, tile_w):
	"""
	Given a center screen position and a tile width, return the top-left screen
	point of the tile for surface drawing.
	"""
	x, y = screen_p
	tile_h = tile_w // 2
	return (x - (tile_w // 2), y - (tile_h // 2))
