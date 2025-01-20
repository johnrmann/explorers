"""
We pre-render sets of terrain tiles, or "chunks", for faster performance
at wider zooms.
"""

import pygame
import line_profiler

from dataclasses import dataclass

from src.math.direction import (
	Direction,
	direction_rotate_90,
	direction_to_delta,
	left_wall_direction,
	right_wall_direction,
)
from src.math.vector2 import Vector2
from src.rendermath.cell import (
	cell_origin_on_global_screen,
	cell_position_on_global_screen
)
from src.rendermath.order import cells_draw_order
from src.rendermath.terrain import TERRAIN_STEPS_PER_CELL
from src.rendermath.tile import tile_z_for_width
from src.world.terrain import Terrain

from src.render.terrain_helper import TerrainSurfacer



@dataclass(frozen=True)
class ChunkSurfaceKey:
	"""How to render the chunk."""
	orientation: Direction
	light: int
	tile_width: int



@dataclass
class ChunkBounds:
	"""
	Represents the bounds of a chunk in cell space.
	"""

	origin: Vector2
	size: int

	cells: set[Vector2] = None

	def __post_init__(self):
		self.cells = set()
		for y in range(self.size):
			for x in range(self.size):
				self.cells.add(Vector2(self.origin) + Vector2(x, y))


	def shift_left_cells(self, cam_dir: Direction = Direction.NORTHWEST):
		lw_dir = left_wall_direction(cam_dir)
		lw_delta = Vector2(direction_to_delta(lw_dir))
		for cell in self.cells:
			yield cell + lw_delta


	def shift_right_cells(self, cam_dir: Direction = Direction.NORTHWEST):
		rw_dir = right_wall_direction(cam_dir)
		rw_delta = Vector2(direction_to_delta(rw_dir))
		for cell in self.cells:
			yield cell + rw_delta


	def top_corner(self, cam_dir: Direction = Direction.NORTHWEST) -> Vector2:
		"""
		Returns the top corner of the chunk in screen space.
		"""
		if cam_dir == Direction.NORTHWEST:
			return Vector2(self.origin)
		ox, oy = self.origin
		if cam_dir == Direction.NORTHEAST:
			return Vector2((ox + self.size - 1, oy))
		if cam_dir == Direction.SOUTHEAST:
			return Vector2((ox + self.size - 1, oy + self.size - 1))
		if cam_dir == Direction.SOUTHWEST:
			return Vector2((ox, oy + self.size - 1))
		raise ValueError(f"Invalid direction: {cam_dir}")


	def bottom_corner(self, cam_dir: Direction = Direction.NORTHWEST) -> Vector2:
		"""
		Returns the bottom corner of the chunk in screen space.
		"""
		ox, oy = self.origin
		if cam_dir == Direction.NORTHWEST:
			return Vector2((ox + self.size - 1, oy + self.size - 1))
		raise ValueError(f"Invalid direction: {cam_dir}")


	def inner_wall_cells(self, cam_dir: Direction = Direction.NORTHWEST):
		"""
		Returns the cell coordinates of the inner wall of the chunk.
		"""
		top = self.top_corner(cam_dir)

		rw_dir = right_wall_direction(cam_dir)
		rw_delta = Vector2(direction_to_delta(rw_dir))
		rw_translate = direction_rotate_90(rw_dir)
		rw_translate_delta = Vector2(direction_to_delta(rw_translate))

		rw_start = top + (rw_delta * (self.size - 1))
		for i in range(self.size):
			yield rw_start + (rw_translate_delta * i)

		lw_dir = left_wall_direction(cam_dir)
		lw_delta = Vector2(direction_to_delta(lw_dir))
		lw_translate = direction_rotate_90(lw_dir)
		lw_translate_delta = Vector2(direction_to_delta(lw_translate))

		lw_start = rw_start + (lw_delta * (self.size - 1))
		for i in range(self.size):
			yield lw_start + (lw_translate_delta * i)


	def outer_wall_cells(self, cam_dir: Direction = Direction.NORTHWEST):
		"""
		Returns the cell coordinates of the outer wall of the chunk.
		"""
		top = self.top_corner(cam_dir)

		rw_dir = right_wall_direction(cam_dir)
		rw_delta = Vector2(direction_to_delta(rw_dir))
		rw_translate = direction_rotate_90(rw_dir)
		rw_translate_delta = Vector2(direction_to_delta(rw_translate))

		rw_start = top + (rw_delta * self.size)
		for i in range(self.size):
			yield rw_start + (rw_translate_delta * i)

		lw_dir = left_wall_direction(cam_dir)
		lw_delta = Vector2(direction_to_delta(lw_dir))
		lw_translate = direction_rotate_90(lw_dir)
		lw_translate_delta = Vector2(direction_to_delta(lw_translate))

		lw_start = top + (rw_delta * (self.size - 1)) + (lw_delta * self.size)
		for i in range(self.size):
			yield lw_start + (lw_translate_delta * i)



class Chunk:
	"""
	A chunk is a square sub-grid of the terrain, pre-rendered for faster game
	rendering.	
	"""

	terrain: Terrain = None
	bounds: ChunkBounds = None

	terrain_surfacer: TerrainSurfacer = None

	_surfaces: dict[ChunkSurfaceKey, pygame.Surface] = None
	_positions: dict[ChunkSurfaceKey, Vector2] = None

	_get_ridge_type: callable = None

	def __init__(
			self,
			terrain: Terrain = None,
			bounds: ChunkBounds = None,
			terrain_surfacer: TerrainSurfacer = None,
			get_ridge_type: callable = None
	):
		self.terrain = terrain
		self.terrain_surfacer = terrain_surfacer
		self.bounds = bounds
		if get_ridge_type is None:
			self._get_ridge_type = self._default_get_ridge_type
		else:
			self._get_ridge_type = get_ridge_type
		self._surfaces = {}
		self._positions = {}
		self._max_height = 0


	def _default_get_ridge_type(self, cell_pos: Vector2, direction: Direction):
		return 0


	def _at_world_edge(self, cam_dir: Direction = Direction.NORTHWEST):
		_, bottom_y = self.bounds.bottom_corner(cam_dir)
		return bottom_y == self.terrain.height - 1


	def is_unobstructed_internally(
			self,
			cam_dir: Direction = Direction.NORTHWEST
	):
		"""
		A chunk is unobstructed internally if no terrain cell obstructs
		another inside the chunk.
		"""
		dummy_bounds = ChunkBounds(self.bounds.origin, self.bounds.size - 1)
		check_lefts = dummy_bounds.shift_left_cells(cam_dir)
		check_rights = dummy_bounds.shift_right_cells(cam_dir)
		compares = dummy_bounds.cells
		for compare, left, right in zip(compares, check_lefts, check_rights):
			if self.terrain.height_at(left) > self.terrain.height_at(compare):
				return False
			if self.terrain.height_at(right) > self.terrain.height_at(compare):
				return False
		return True


	def is_unobstructed_externally(
			self,
			cam_dir: Direction = Direction.NORTHWEST
	):
		"""
		A chunk is unobstructed externally if no terrain cell obstructs the
		outside of this chunk.
		"""
		check_lefts = self.bounds.shift_left_cells(cam_dir)
		check_rights = self.bounds.shift_right_cells(cam_dir)
		compares = self.bounds.cells
		for compare, left, right in zip(compares, check_lefts, check_rights):
			if self.terrain.height_at(left) > self.terrain.height_at(compare):
				return False
			if self.terrain.height_at(right) > self.terrain.height_at(compare):
				return False
		return True


	def wall_height(self, cam_dir: Direction = Direction.NORTHWEST):
		"""
		Returns the height of the walls of the chunk.
		"""
		if self._at_world_edge(cam_dir):
			return self._max_height
		inners = self.bounds.inner_wall_cells(cam_dir)
		outers = self.bounds.outer_wall_cells(cam_dir)
		max_height = 0
		for inner, outer in zip(inners, outers):
			ih = self.terrain.height_at(inner)
			oh = self.terrain.height_at(outer)
			max_height = max(0, max_height, ih - oh)
		return max_height


	def get_rect(
			self,
			cam_dir: Direction = Direction.NORTHWEST,
			tile_width: int = 64,
	):
		"""
		Returns the dimensions of the surface for this chunk.
		"""
		tile_height = tile_width // 2
		tile_z = tile_z_for_width(tile_width)
		terrain_z = tile_z / TERRAIN_STEPS_PER_CELL

		surface_width = self.bounds.size * tile_width

		wall_height_steps = self.wall_height(cam_dir)
		wall_height_px = wall_height_steps * terrain_z

		# Remember that y=0 is at the top of the screen.
		tile_top_px = 999_999_999
		tile_bottom_px = -1
		tile_left_px = 999_999_999
		origin = Vector2(self.bounds.origin)
		for y in range(self.bounds.size):
			for x in range(self.bounds.size):
				cell_pos = origin + Vector2(x, y)
				h = self.terrain.height_at(cell_pos)
				tl_x, tl_y = cell_origin_on_global_screen(cell_pos, cam_dir, tile_width)
				cell_top_px = tl_y - (h * terrain_z)
				cell_bottom_px = cell_top_px + tile_height
				cell_left_px = tl_x
				tile_top_px = min(tile_top_px, cell_top_px)
				tile_bottom_px = max(tile_bottom_px, cell_bottom_px)
				tile_left_px = min(tile_left_px, cell_left_px)

		tile_diff = tile_bottom_px - tile_top_px
		surface_height = tile_diff + max(wall_height_px, 0)

		return (
			Vector2(tile_left_px, tile_top_px),
			(surface_width, surface_height),
		)


	def draw_order(self, cam_dir: Direction = Direction.NORTHWEST):
		"""
		Returns the draw order for the chunk.
		"""
		return cells_draw_order(
			self.bounds.origin,
			self.bounds.size,
			cam_dir
		)


	def draws(self, key: ChunkSurfaceKey = None):
		lw_dir = left_wall_direction(key.orientation)
		rw_dir = right_wall_direction(key.orientation)
		for position in self.draw_order(cam_dir=key.orientation):
			ox, oy = cell_position_on_global_screen(
				position,
				key.orientation,
				(key.tile_width, key.tile_width // 2)
			)
			x, y = position
			ox -= key.tile_width // 2
			oy -= key.tile_width // 4
			land_height = self.terrain.land_height_at(position)
			wall_thickness = max(
				self.terrain.height_delta(position, lw_dir),
				self.terrain.height_delta(position, rw_dir),
				0
			)
			draws = self.terrain_surfacer.draws(
				land_height=land_height,
				land_visible=True,
				is_frozen=self.terrain.is_cell_ice(position),
				water_height=self.terrain.height_at(position) - land_height,
				tile_size=key.tile_width,
				light=key.light,
				ridges=self._get_ridge_type((x,y), key.orientation),
				delta_height=wall_thickness
			)
			for h, surface in draws:
				yield (ox, oy + h), surface


	def _render(
			self,
			key: ChunkSurfaceKey = None
	):
		if key is None:
			raise ValueError("key must be provided")
		cam_dir = key.orientation
		tile_width = key.tile_width

		global_pos, surface_dims = self.get_rect(
			cam_dir=cam_dir,
			tile_width=tile_width
		)
		self._positions[key] = global_pos

		surface = pygame.Surface(surface_dims).convert_alpha()
		surface.fill((0, 0, 0, 0))
		for draw_pos, tile_surface in self.draws(key=key):
			local_tile_pos = Vector2(draw_pos) - global_pos
			local_x, local_y = local_tile_pos
			surface.blit(tile_surface, (local_x, local_y))
		self._surfaces[key] = surface


	def _get_surface(
			self,
			key: ChunkSurfaceKey = None
	):
		if key in self._surfaces:
			return self._surfaces[key]
		else:
			self._render(key=key)
			return self._surfaces[key]


	def get_draw(
			self,
			tile_width: int = 64,
			light: int = 7,
			camera_orientation: Direction = Direction.NORTHWEST,
	):
		"""
		Get the (global screen position, surface) for the given draw parameters.
		"""
		key = ChunkSurfaceKey(
			orientation=camera_orientation,
			light=light,
			tile_width=tile_width
		)
		surface = self._get_surface(key=key)
		position = self._positions[key]
		return position, surface



class TerrainChunker:
	"""
	Coordinates the pre-rendering of terrain "chunks" for fastrer rendering.
	"""

	_terrain: Terrain = None
	_terrain_surfacer: TerrainSurfacer = None

	_chunk_size: int = 16

	_chunks: dict[tuple[int, int], Chunk] = None

	_dirty: set[tuple[int, int]] = None
	_dirties_per_render: int = 5

	_get_ridge_type: callable = None

	def __init__(
			self,
			terrain: Terrain = None,
			surfacer: TerrainSurfacer = None,
			chunk_size: int = 8,
			get_ridge_type: callable = None
	):
		self._terrain = terrain
		self._terrain_surfacer = surfacer
		self._chunk_size = chunk_size
		self._chunks = {}
		self._dirty = set()
		self._get_ridge_type = get_ridge_type


	def get_chunks(self):
		"""
		Returns all the chunks in the chunker, clean or dirty.
		"""
		return set(self._chunks.values())


	def all_chunk_origins(self):
		"""
		Returns the origins of all the chunks in the chunker.
		"""
		for y in range(self._terrain.height // self._chunk_size):
			for x in range(self._terrain.width // self._chunk_size):
				yield Vector2(x * self._chunk_size, y * self._chunk_size)


	def chunk_index_for_cell(self, cell_pos: Vector2) -> tuple[int, int]:
		"""
		Returns the chunk index for the given cell position.
		"""
		x, y = cell_pos
		return (
			(x % self._terrain.width) // self._chunk_size,
			y // self._chunk_size
		)


	def mark_cell_dirty(self, cell_pos: Vector2):
		"""
		Mark a cell as dirty.
		"""
		chunk_index = self.chunk_index_for_cell(cell_pos)
		self._dirty.add(chunk_index)


	def is_cell_dirty(self, cell_pos: Vector2) -> bool:
		"""
		Is the cell dirty?
		"""
		chunk_index = self.chunk_index_for_cell(cell_pos)
		return chunk_index in self._dirty


	def get_chunk(self, cell_pos: Vector2):
		"""
		Returns the surface for the chunk that contains the given cell.
		"""
		chunk_index = self.chunk_index_for_cell(cell_pos)
		if chunk_index in self._dirty:
			return None
		if chunk_index not in self._chunks:
			self._dirty.add(chunk_index)
			return None
		return self._chunks[chunk_index]


	def make_chunk(self, cell_pos: Vector2):
		"""
		Create a chunk for the given cell.
		"""
		chunk_index = self.chunk_index_for_cell(cell_pos)
		if chunk_index in self._chunks:
			return self._chunks[chunk_index]
		chunk_origin = Vector2(
			chunk_index[0] * self._chunk_size,
			chunk_index[1] * self._chunk_size
		)
		chunk_bounds = ChunkBounds(chunk_origin, self._chunk_size)
		chunk = Chunk(
			terrain=self._terrain,
			bounds=chunk_bounds,
			terrain_surfacer=self._terrain_surfacer,
			get_ridge_type=self._get_ridge_type
		)
		self._chunks[chunk_index] = chunk
		return chunk


	def make_all_chunks(self):
		"""
		Make all chunks in the chunker.
		"""
		for origin in self.all_chunk_origins():
			self.make_chunk(origin)


	def chunks_intersecting_rect(self, rect: tuple[Vector2, Vector2]):
		"""
		Returns the chunks that intersect the given rectangle (origin, size).
		
		Remember: a size=1,1 means a 1x1 rectangle consisting of just the
		origin!
		"""
		origin, size = rect
		ox, oy = origin
		sx, sy = size
		min_x_idx = ox // self._chunk_size
		min_y_idx = oy // self._chunk_size
		max_x_idx = ((ox + sx - 1) // self._chunk_size) + 1
		max_y_idx = ((oy + sy - 1) // self._chunk_size) + 1
		for x in range(min_x_idx, max_x_idx):
			for y in range(min_y_idx, max_y_idx):
				yield self.get_chunk(
					(x * self._chunk_size, y * self._chunk_size)
				)
