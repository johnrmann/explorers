import pygame

from dataclasses import dataclass

from src.math.line import extrude_line_segment_y

from src.render.multisurface import MultiSurface

from src.render.utils import scale_color
from src.rendermath.terrain import terrain_step_z_for_tile_width
from src.rendermath.tile import tile_polygon
from src.render.viewport import ZOOMS

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


class TileColors:
	__slots__ = ('top_color', 'left_color', 'right_color')

	top_color: tuple[int, int, int]
	left_color: tuple[int, int, int]
	right_color: tuple[int, int, int]

	def __init__(self, top_color=None, left_color=None, right_color=None):
		if top_color is None:
			raise ValueError('Top color must be provided.')
		if left_color is None:
			left_color = scale_color(top_color, 0.5)
		if right_color is None:
			right_color = scale_color(top_color, 0.25)
		self.top_color = top_color
		self.left_color = left_color
		self.right_color = right_color


class TileSurfaceCache:
	"""
	Pre-render diagonal tiles and their walls at different zooms and heights
	for faster rendering.
	"""

	# This is mostly used for debug purposes.
	_name: str

	_top_color: tuple[int, int, int]
	_left_color: tuple[int, int, int]
	_right_color: tuple[int, int, int]

	_jut = None

	zooms: list[int]

	def __init__(self, zooms=None, colors=None, name=None):
		self._name = name

		if zooms is None:
			zooms = ZOOMS

		if colors is None:
			colors = TileColors(
				top_color=GROUND_COLOR,
				left_color=WALL_COLOR_1,
				right_color=WALL_COLOR_2,
			)
		self._top_color = colors.top_color
		self._left_color = colors.left_color
		self._right_color = colors.right_color

		self.zooms = zooms
		self._init_jut()


	def _make_tile_and_surface(self, tile_width, thickness=0):
		z = terrain_step_z_for_tile_width(tile_width) * thickness
		h = tile_width // 2
		dims = (tile_width, h + z)
		surface = pygame.Surface(dims, pygame.SRCALPHA).convert_alpha()
		tile = tile_polygon((tile_width // 2, h // 2), (tile_width, h))
		pygame.draw.polygon(surface, self._top_color, tile)

		# Now draw the tile's walls.
		if thickness != 0:
			left_wall = _wall_for_direction_height_zoom('left', 8, tile_width)
			right_wall = _wall_for_direction_height_zoom('right', 8, tile_width)
			pygame.draw.polygon(surface, self._left_color, left_wall)
			pygame.draw.polygon(surface, self._right_color, right_wall)

		return tile, surface


	def _make_tile_multisurface(
			self,
			left_ridge=False,
			right_ridge=False,
			thickness=0
	):
		tilesurfs = [
			self._make_tile_and_surface(zoom, thickness=thickness) + (zoom,)
			for zoom in self.zooms
		]
		for tile, surface, _ in tilesurfs:
			tile_top, tile_right, _, tile_left = tile
			if left_ridge:
				pygame.draw.line(
					surface, self._left_color, tile_left, tile_top
				)
			if right_ridge:
				pygame.draw.line(
					surface, self._right_color, tile_top, tile_right
				)
		zoomed_surfaces = {
			zoom: surface
			for _, surface, zoom in tilesurfs
		}
		return MultiSurface(
			zoomed_surfaces=zoomed_surfaces,
		)


	def _init_jut(self):
		self._jut = {}
		for ridges in (NO_RIDGES, LEFT_RIDGE, RIGHT_RIDGE, BOTH_RIDGES):
			for thickness in range(9):
				self._jut[ridges, thickness] = self._make_tile_multisurface(
					left_ridge=(ridges & LEFT_RIDGE) != 0,
					right_ridge=(ridges & RIGHT_RIDGE) != 0,
					thickness=thickness
				)


	def tile_surface(self, tile_width=64, thickness=0, ridges=NO_RIDGES, light=7):
		"""
		Given a position on the screen that is the center of the tile we want
		to draw and the zoom factor, return the tile surface and blit position
		(top left corner).
		"""
		idx = int(tile_width)
		sub_cache = self._jut[ridges, thickness]
		surface = sub_cache.get(idx, light=light)
		return surface
