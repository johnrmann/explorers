import pygame

from src.math.line import extrude_line_segment_y

from src.render.multisurface import MultiSurface

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

	tile_multisurface: MultiSurface
	left_ridge_multisurface: MultiSurface
	right_ridge_multisurface: MultiSurface
	both_ridge_multisurface: MultiSurface

	_jut = None

	zooms: list[int]

	def __init__(self, zooms=None):
		if zooms is None:
			zooms = ZOOMS
		self.zooms = zooms
		self.tile_multisurface = self._make_tile_multisurface()
		self.left_ridge_multisurface = self._make_tile_multisurface(left_ridge=True)
		self.right_ridge_multisurface = self._make_tile_multisurface(right_ridge=True)
		self.both_ridge_multisurface = self._make_tile_multisurface(left_ridge=True, right_ridge=True)
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

	def _make_tile_multisurface(self, left_ridge=False, right_ridge=False):
		tilesurfs = [
			self._make_tile_and_surface(zoom) + (zoom,)
			for zoom in self.zooms
		]
		for tile, surface, zoom in tilesurfs:
			tile_top, tile_right, _, tile_left = tile
			if left_ridge:
				pygame.draw.line(surface, WALL_COLOR_1, tile_left, tile_top)
			if right_ridge:
				pygame.draw.line(surface, WALL_COLOR_1, tile_top, tile_right)
		zoomed_surfaces = {
			zoom: surface
			for _, surface, zoom in tilesurfs
		}
		return MultiSurface(
			zoomed_surfaces=zoomed_surfaces,
		)

	def _init_jut(self):
		self._jut = {
			NO_RIDGES: self.tile_multisurface,
			LEFT_RIDGE: self.left_ridge_multisurface,
			RIGHT_RIDGE: self.right_ridge_multisurface,
			BOTH_RIDGES: self.both_ridge_multisurface
		}

	def tile_surface_and_position(self, screen_p, zoom, ridges=None, light=None):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw and the zoom factor, return the tile surface and blit position
		(top left corner).
		"""
		idx = int(zoom)
		if ridges is None:
			ridges = NO_RIDGES
		sub_cache = self._jut[ridges]
		surface = sub_cache.get(idx, light=light)
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
