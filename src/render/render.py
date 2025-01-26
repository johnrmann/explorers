import line_profiler
import pygame

from collections import defaultdict

from src.gameobject.gameobject import GameObject

from src.rendermath.order import screen_draw_order
from src.rendermath.draw_graph import DrawGraph
from src.rendermath.fit_rect import (
	object_height_from_img_dims,
	fit_img_rect_on_tile_base
)
from src.rendermath.box import Box
from src.rendermath.multicell import multicell_polygon_on_global_screen

from src.world.world import World

from src.render.multisurface import (
	MAX_LIGHT_LEVEL_IDX, MultiSurface, LIGHT_LEVELS
)
from src.render.viewport import Viewport
from src.render.terrain_helper import TerrainHelper
from src.render.utils import height_offset_tile, box_between_tiles
from src.render.render_order import RenderOrder
from src.render.chunk import TerrainChunker, Chunk

IMG_PATHS = [
	'assets/img/sprite/astronaut-cropped.png',
	'assets/img/sprite/lander.png',
	'assets/img/sprite/click-here.png',
	'assets/img/sprite/flag.png',
	'assets/img/sprite/palm-tree.png',
]

HIGHLIGHT_COLOR = (0, 250, 0)

NO_GOBJ_IMAGE_TOP_COLOR = (0, 0, 200)
NO_GOBJ_IMAGE_LEFT_COLOR = (0, 0, 100)
NO_GOBJ_IMAGE_RIGHT_COLOR = (0, 0, 50)



class Render:
	"""
	Renders the game.
	"""

	_last_zoom = 0

	_highlight_colors: dict[tuple[int, int], tuple[int, tuple]] = None

	_brightnesses = None

	_chunker: TerrainChunker

	def __init__(self, window, world: World, vp: Viewport, game_mgr=None):
		self.game_mgr = game_mgr
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = TerrainHelper(world.terrain, vp)
		self._highlight_colors = defaultdict(lambda: None)
		self._chunker = TerrainChunker(
			terrain=world.terrain,
			surfacer=self.render_terrain.terrain_surfacer,
			get_ridge_type=self.render_terrain.get_ridge_type,
		)
		self._load_images()
		self._calc_draw_order()
		self._calc_brightnesses()
		self._chunker.make_all_chunks()


	def _load_images(self):
		self.images = {}
		self.image_z_factors = {}
		for path in IMG_PATHS:
			surface = pygame.image.load(path).convert_alpha()
			multisurface = MultiSurface(
				surface,
				alpha_color=(255, 255, 255, 255),
				zoom_factors=[1.0],
				lights=LIGHT_LEVELS
			)
			self.images[path] = multisurface
			img_dims = object_height_from_img_dims(surface.get_size())
			self.image_z_factors[path] = img_dims


	def _calc_draw_order(self):
		self._last_zoom = self.vp.tile_width
		self.draw_order = list(screen_draw_order(
			(0, 0),
			self.vp.camera_orientation,
			self.vp.tiles_wide,
			2 * self.vp.tiles_tall
		))


	def _calc_brightnesses(self):
		self._brightnesses = {}
		for idx, long in enumerate(self.world.terrain.longs):
			self._brightnesses[idx] = self.world.horology.brightness(
				0, long
			)


	def _render_game_object(self, go: GameObject=None, light = None):
		# Easy out if the gameobject is hidden
		if go.hidden:
			return

		cam_ori = self.vp.camera_orientation
		tile_dims = self.vp.tile_dimensions
		terrain = self.world.terrain
		clickmap = self.game_mgr.clickmap

		# A "cell polygon" is the position of the tile if there was no terrain.
		multicell_polygon_global = multicell_polygon_on_global_screen(
			go.draw_bounds, cam_ori, tile_dims
		)
		multicell_polygon = [
			self.vp.global_screen_position_to_screen_position(p)
			for p in multicell_polygon_global
		]
		height = terrain.height_at(go.pos)
		base_polygon = height_offset_tile(
			multicell_polygon, height / 8, self.vp
		)

		if go.image_path() in self.images:
			img = self.images[go.image_path()].get(light=light)
			alpha = self.images[go.image_path()].get_alpha()
			origin, img_dims = fit_img_rect_on_tile_base(
				img.get_size(), base_polygon
			)
			self.window.blit(
				pygame.transform.scale(img, img_dims),
				pygame.Rect(origin, img_dims),
			)
			clickmap.mark_game_object(
				go, origin, pygame.transform.scale(alpha, img_dims)
			)
		else:
			top = height_offset_tile(base_polygon, 1, self.vp)
			top_poly, left, right = box_between_tiles(top, base_polygon)
			pygame.draw.polygon(self.window, NO_GOBJ_IMAGE_TOP_COLOR, top_poly)
			pygame.draw.polygon(self.window, NO_GOBJ_IMAGE_LEFT_COLOR, left)
			pygame.draw.polygon(self.window, NO_GOBJ_IMAGE_RIGHT_COLOR, right)


	def bounding_box_for_gameobject(self, go):
		"""
		Use the game object's position and size to compute its bounding box
		on the screen.

		If the game object's size is 2D, use its image as the basis for its
		height. Otherwise, use the third element of its size tuple.

		If the game object's size is 2D and there is no image, just use zero
		for height.
		"""
		pos = go.pos3
		w, d, h = go.size
		if h is None:
			img_path = go.image_path()
			if img_path in self.image_z_factors:
				h = self.image_z_factors[img_path] * w
			else:
				h = 0
		return Box(p=pos, size=(w, d, h))


	def render_tile(self, cell_pos, light=MAX_LIGHT_LEVEL_IDX):
		draws = self.render_terrain.tile_draws(cell_pos, light=light)
		for draw_pos, surface in draws:
			local_draw_pos = self.vp.global_screen_position_to_screen_position(draw_pos)
			self.window.blit(surface, surface.get_rect(topleft=local_draw_pos))


	def _render_chunk(self, chunk: Chunk, light):
		global_pos, surface = chunk.get_draw(
			tile_width=self.vp.tile_width,
			light=light,
			camera_orientation=self.vp.camera_orientation
		)
		draw_pos = self.vp.global_screen_position_to_screen_position(global_pos)
		self.window.blit(surface, draw_pos)


	def cells_to_draw(self):
		"""
		Returns all cells that should be drawn.
		"""
		terrain_height = self.vp.terrain_height
		ox, oy = self.vp.get_draw_origin()
		draw_order = map(
			lambda p: (p[0] + ox, p[1] + oy),
			self.draw_order
		)
		safe_draw_order = filter(
			lambda p: 0 <= p[1] < terrain_height,
			draw_order
		)
		return safe_draw_order


	@line_profiler.profile
	def render_order(self) -> RenderOrder:
		"""
		Returns a list of RenderTuples that represent the order in which
		stuff should be rendered.
		"""
		order = RenderOrder()

		clean_chunks = self._chunker.get_chunks()

		pre_go_draw_graph = {
			go: self.bounding_box_for_gameobject(go)
			for go in self.game_mgr.game_objects
		}
		draw_graph = DrawGraph(key_vals=pre_go_draw_graph)

		cam_ori = self.vp.camera_orientation
		game_mgr_utc = self.game_mgr.utc
		horology = self.world.horology
		terrain_width = self.vp.terrain_width
		cycle_frac = game_mgr_utc / horology.ticks_in_cycle
		time_offset = int((cycle_frac % 1) * terrain_width)
		_brightnesses = self._brightnesses
		get_chunk = self._chunker.get_chunk

		time_offset_bnesses = {
			x: _brightnesses[(x + time_offset) % terrain_width]
			for x in range(-terrain_width, terrain_width * 3)
		}
		c_size = self._chunker.chunk_size

		check_chunks = clean_chunks.copy()
		for chunk in check_chunks:
			light_west = time_offset_bnesses[chunk.bounds.origin.x]
			light_east = time_offset_bnesses[chunk.bounds.origin.x + c_size]
			if light_west != light_east:
				clean_chunks.remove(chunk)

		gobjs_by_draw_pos = {
			go.draw_point(cam_ori): go
			for go in self.game_mgr.game_objects
		}
		clean_chunks -= set(
			self._chunker.chunks_intersecting_rect(gobj.rect)
			for gobj in self.game_mgr.game_objects
		)

		for x, y in self.cells_to_draw():
			p = (x, y)
			brightness = time_offset_bnesses[x]

			if p not in order:
				chunk = get_chunk(p)
				if chunk in clean_chunks:
					order.add_chunk(chunk, brightness=brightness)
					clean_chunks.remove(chunk)
				else:
					order.add_cell(p, brightness=brightness)

			if p in gobjs_by_draw_pos:
				gobj = gobjs_by_draw_pos[p]
				to_draw = draw_graph.get_draws(gobj)
				for draw_gobj in to_draw:
					order.add_game_object(draw_gobj, brightness=brightness)
					draw_graph.mark_drawn(draw_gobj)
			
			if tuple(p) in self._highlight_colors:
				order.add_highlight_cell(p)

		return order


	@line_profiler.profile
	def render(self):
		if self.vp.tile_width != self._last_zoom:
			self._calc_draw_order()

		self.window.fill((0,0,200))

		order = self.render_order()
		render_tile = self.render_tile
		render_gobj = self._render_game_object
		render_chunk = self._render_chunk

		for to_draw in order:
			if to_draw.cell:
				render_tile(to_draw.cell, light=to_draw.brightness)
			elif to_draw.highlight_cell:
				self._draw_highlight_tile(to_draw.highlight_cell)
			elif to_draw.game_object:
				render_gobj(to_draw.game_object, light=to_draw.brightness)
			elif to_draw.chunk:
				render_chunk(to_draw.chunk, light=to_draw.brightness)


	def _draw_highlight_tile(
			self,
			tile_p: tuple[int, int] = None,
	):
		if tile_p not in self._highlight_colors:
			return
		_, color = self._highlight_colors[tile_p]
		top = self.render_terrain.tile_top_polygon(tile_p)
		for p1_idx in range(4):
			p2_idx = (p1_idx + 1) % 4
			p1 = top[p1_idx]
			p2 = top[p2_idx]
			pygame.draw.line(self.window, color, p1, p2)


	def highlight_tile(
			self,
			tile_p: tuple[int, int] = None,
			color=HIGHLIGHT_COLOR,
			priority=1
	):
		"""
		Draws a green border around the tile at the given position.
		"""
		if not tile_p:
			return
		pair = self._highlight_colors[tile_p]
		if not pair:
			self._highlight_colors[tile_p] = (priority, color)
		else:
			curr_priority, _ = pair
			if priority > curr_priority:
				self._highlight_colors[tile_p] = (priority, color)


	def highlight_tile_at_screen_pos(self, screen_pos: tuple[int, int] = None):
		"""
		Highlights the tile at the given position.
		"""
		return self.highlight_tile(
			tile_p=self.render_terrain.tile_at_screen_pos(screen_pos),
		)


	def clear(self):
		"""
		Call once per frame.
		"""
		self._highlight_colors.clear()
