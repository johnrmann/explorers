from src.world.terrain import Terrain

from src.math.direction import (
	DIAGONAL_DIRECTIONS,
	Direction,
	left_ridge_direction,
	right_ridge_direction,
	left_wall_direction,
	right_wall_direction,
	direction_to_delta
)
from src.math.vector2 import Vector2

from src.rendermath.tile import (
	tile_polygon,
	is_point_in_tile,
	is_tile_in_screen,
	tile_z_for_width
)
from src.rendermath.order import offset_tile_by_draw_order_vector
from src.rendermath.geometry import is_point_in_screen

from src.render.tile_surface import NO_RIDGES, TileSurfaceCache, TileColors
from src.render.multisurface import MAX_LIGHT_LEVEL_IDX
from src.render.viewport import Viewport
from src.render.utils import height_offset_tile

class TerrainSurfacer:
	"""
	This class is responsible for returning the surfaces for the terrain, and
	the height offsets at which to draw them.

	Do not instantiate more than one of these, as creating the different tile
	caches is expensive (four sizes times eight light levels).
	"""

	land_cache: TileSurfaceCache
	water_cache: TileSurfaceCache
	ice_cache: TileSurfaceCache

	_terrain_thicknesses: dict[int, int] = None

	def __init__(self):
		self._terrain_thicknesses = {
			128: tile_z_for_width(128) / 8,
			64: tile_z_for_width(64) / 8,
			32: tile_z_for_width(32) / 8,
			16: tile_z_for_width(16) / 8,
		}
		self.land_cache = TileSurfaceCache(name='land')
		self.water_cache = TileSurfaceCache(
			colors=TileColors(
				top_color=(0, 0, 200),
				left_color=(0, 0, 150),
				right_color=(0, 0, 100)
			),
			name='water'
		)
		self.ice_cache = TileSurfaceCache(
			colors=TileColors(
				top_color=(200, 200, 200),
				left_color=(150, 150, 150),
				right_color=(100, 100, 100)
			),
			name='ice'
		)


	def draws(
			self,
			land_height: int = 0,
			land_visible: bool = True,
			water_height: int = 0,
			is_frozen: bool = False,
			light: int = MAX_LIGHT_LEVEL_IDX,
			tile_size: int = 64,
			ridges: int = NO_RIDGES,
			delta_height: int = 0
	):
		"""
		Get all pairs of height offset and surface to draw for the given
		tile configuration.
		"""
		terrain_thickness = self._terrain_thicknesses[tile_size]
		h = -land_height * terrain_thickness
		if land_visible:
			land_surface = self.land_cache.tile_surface(
				tile_width=tile_size, ridges=ridges, light=light, thickness=min(delta_height, 8)
			)
			yield h, land_surface
		h -= water_height * terrain_thickness
		if water_height:
			layer_cache = self.ice_cache if is_frozen else self.water_cache
			water_surface = layer_cache.tile_surface(
				tile_width=tile_size, ridges=ridges, light=light, thickness=min(delta_height, 8)
			)
			yield h, water_surface



class TerrainHelper:
	"""
	The purpose of this class is to calculate draw positions and draw surfaces
	for the terrain.
	"""

	_all_ridge_draws: dict[Direction, dict[tuple[int, int], int]]
	_ridge_draws: dict[tuple[int, int], int]

	_land_visibility: dict[tuple[int, int], bool]

	terrain: Terrain
	vp: Viewport

	terrain_surfacer: TerrainSurfacer = None

	def __init__(self, terrain: Terrain, vp: Viewport):
		self.terrain = terrain
		self.vp = vp
		self.terrain_surfacer = TerrainSurfacer()
		self._calc_ridges()
		self._calc_land_visibility()
		self._calc_wall_thicknesses()


	def _calc_ridge(self, cell_pos, direction: Direction):
		left = self.terrain.height_delta(
			cell_pos, left_ridge_direction(direction)
		)
		right = self.terrain.height_delta(
			cell_pos, right_ridge_direction(direction)
		)
		left_bit = (left > 0) & 1
		right_bit = (right > 0) << 1
		return left_bit | right_bit


	def get_ridge_type(self, cell_pos, direction: Direction):
		"""
		Returns the ridge type at the given cell position.
		"""
		return self._all_ridge_draws[direction][cell_pos]


	def _calc_ridges(self):
		self._all_ridge_draws = {}
		for d in DIAGONAL_DIRECTIONS:
			self._all_ridge_draws[d] = {}
			for y in range(self.terrain.height):
				for x in range(self.terrain.width):
					p = (x, y)
					self._all_ridge_draws[d][p] = self._calc_ridge(p, d)
		self._ridge_draws = self._all_ridge_draws[self.vp.camera_orientation]


	def _calc_land_visibility(self):
		self._land_visibility = {}
		for y in range(self.terrain.height):
			for x in range(self.terrain.width):
				self._land_visibility[(x, y)] = self.land_visible_at((x, y))


	def _calc_wall_thicknesses_for_cell_in_dir(self, cell_pos, direction):
		lw_dir = left_wall_direction(direction)
		rw_dir = right_wall_direction(direction)
		left = self.terrain.height_delta(cell_pos, lw_dir)
		right = self.terrain.height_delta(cell_pos, rw_dir)
		return max(left, right, 0)


	def _calc_wall_thicknesses_for_dir(self, direction):
		thicknesses = {}
		sub_fun = self._calc_wall_thicknesses_for_cell_in_dir
		for y in range(self.terrain.height):
			for x in range(self.terrain.width):
				thicknesses[(x, y)] = sub_fun((x, y), direction)
		return thicknesses


	def _calc_wall_thicknesses(self):
		self._wall_thicknesses = {}
		for d in DIAGONAL_DIRECTIONS:
			self._wall_thicknesses[d] = self._calc_wall_thicknesses_for_dir(d)


	def tile_bottom_polygon(self, tile_p):
		"""
		Return the polygon of the bottom of the rectangular prism of the tile
		at the given position.
		"""
		tile_screen = self.vp.tile_to_screen_coords(tile_p)
		return tile_polygon(tile_screen, self.vp.tile_dimensions)


	def tile_top_polygon(self, tile_p):
		"""
		Return the polygon of the top of the rectangular prism of the tile
		at the given position.
		"""
		x, y = tile_p
		if not 0 <= y < self.terrain.height:
			return None
		h = self.terrain.map[y][x % self.terrain.width]
		bottom = self.tile_bottom_polygon(tile_p)
		return height_offset_tile(bottom, h / 8, self.vp)


	def land_visible_at(self, cell_pos):
		"""
		Returns whether land is visible at the given cell position.

		The terrain has a land layer and a water layer (that can be either ice
		or water). If water is completely surrounded by water, we don't want
		to draw the land below it to save some performance.
		"""

		if self.terrain.is_cell_land(cell_pos):
			return True
		x, y = cell_pos
		if y == self.terrain.height - 1:
			return True

		lw_dir = left_wall_direction(self.vp.camera_orientation)
		dx_left, dy_left = direction_to_delta(lw_dir)
		left_cell = (x + dx_left, y + dy_left)
		total_left_height = self.terrain.height_at(left_cell)

		rw_dir = right_wall_direction(self.vp.camera_orientation)
		dx_right, dy_right = direction_to_delta(rw_dir)
		right_cell = (x + dx_right, y + dy_right)
		total_right_height = self.terrain.height_at(right_cell)

		land_height = self.terrain.land_height_at(cell_pos)
		return min(total_left_height, total_right_height) < land_height


	def tile_draws(self, cell_pos, light=MAX_LIGHT_LEVEL_IDX):
		"""
		Generates a list of (position, surface) tuples to draw to render the
		tile at the given position.
		"""

		self_terrain = self.terrain

		x, y = cell_pos
		cell_pos_mod = (x % self_terrain.width, y)
		zoom = self.vp.tile_width
		screen_x, screen_y = self.vp.cell_position_on_global_screen(cell_pos)
		screen_x -= (self.vp.tile_width // 2)
		screen_y -= (self.vp.tile_height // 2)
		ridges = self._ridge_draws[cell_pos_mod]

		land_height = self_terrain.land_height_at(cell_pos)
		delta_height = self._wall_thicknesses[self.vp.camera_orientation][cell_pos_mod]
		draws = self.terrain_surfacer.draws(
			land_height=land_height,
			land_visible=self._land_visibility[cell_pos_mod],
			water_height=self_terrain.height_at(cell_pos) - land_height,
			is_frozen=self_terrain.is_cell_ice(cell_pos),
			light=light,
			tile_size=zoom,
			ridges=ridges,
			delta_height=delta_height
		)
		for height_offset, surface in draws:
			pos = (screen_x, screen_y + height_offset)
			yield pos, surface


	def tile_at_screen_pos(self, screen_p):
		"""
		Returns the tile at the current mouse cursor position.
		"""
		win_dims = self.vp.window_dims
		if not is_point_in_screen(screen_p, win_dims):
			return None
		x, y = self.vp.screen_to_tile_coords(screen_p)
		original = Vector2(x, y).round()
		max_h = -1
		found = None
		for direction in [-1, 1]:
			k = 0
			while True:
				p_left, p_right = offset_tile_by_draw_order_vector(
					original,
					self.vp.camera_orientation,
					k * direction
				)
				t_left = self.tile_top_polygon(p_left)
				t_right = self.tile_top_polygon(p_right)
				if not t_left and not t_right:
					break
				l_in_screen = t_left and is_tile_in_screen(t_left, win_dims)
				r_in_screen = t_right and is_tile_in_screen(t_right, win_dims)
				if not l_in_screen and not r_in_screen:
					break
				if t_left and is_point_in_tile(screen_p, t_left):
					h_left = self.terrain.height_at(p_left)
					if h_left > max_h:
						max_h = h_left
						found = p_left
				elif t_right and is_point_in_tile(screen_p, t_right):
					h_right = self.terrain.height_at(p_right)
					if h_right > max_h:
						max_h = h_right
						found = p_right
				k += 1
		return found
