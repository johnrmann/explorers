import pygame

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

IMG_PATHS = [
	'assets/img/astronaut-cropped.png',
	'assets/img/lander.png',
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

	_brightnesses = None

	def __init__(self, window, world: World, vp: Viewport, game_mgr=None):
		self.game_mgr = game_mgr
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = TerrainHelper(world.terrain, vp)
		self.drawn_cells = set()
		self._load_images()
		self._calc_draw_order()
		self._calc_brightnesses()

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

	def game_object_at(self, p):
		for go in self.game_mgr.game_objects:
			gx, gy = go.pos
			x, y = p
			if x == gx and y == gy:
				return go
		return None

	def _render_game_object(self, go: GameObject=None, light = None):
		# Easy out if the gameobject is hidden
		if go.hidden:
			return

		# First, render all terrain tiles below the gobj.
		for p in go.cells_occupied(self.vp.camera_orientation):
			if p in self.drawn_cells:
				continue
			self.render_tile(p, light=light)

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
		_, y = cell_pos
		if y < 0:
			return
		if y >= self.vp.terrain_height:
			return

		draws = self.render_terrain.tile_draws(cell_pos, light=light)
		for draw_pos, surface in draws:
			local_draw_pos = self.vp.global_screen_position_to_screen_position(draw_pos)
			self.window.blit(surface, surface.get_rect(topleft=local_draw_pos))
		self.drawn_cells.add(cell_pos)

	def render(self):
		self.drawn_cells = set()
		if self.vp.tile_width != self._last_zoom:
			self._calc_draw_order()

		self.window.fill((0,0,200))

		pre_go_draw_graph = {
			go: self.bounding_box_for_gameobject(go)
			for go in self.game_mgr.game_objects
		}
		draw_graph = DrawGraph(key_vals=pre_go_draw_graph)

		gobj_cells = {
			go.draw_point(self.vp.camera_orientation): go
			for go in self.game_mgr.game_objects
		}

		ox, oy = self.vp.get_draw_origin()

		# Cache frequently accessed attributes and methods
		horology = self.world.horology
		render_tile = self.render_tile
		game_mgr_utc = self.game_mgr.utc
		terrain_width = self.vp.terrain_width
		terrain_height = self.vp.terrain_height
		cycle_frac = game_mgr_utc / horology.ticks_in_cycle
		time_offset = int(((cycle_frac) % 1) * terrain_width)

		for dx, dy in self.draw_order:
			x = ox + dx
			y = oy + dy
			p = (x, y)
			if not 0 <= y < terrain_height:
				continue
			if p in self.drawn_cells:
				continue
			bness_x = (x + time_offset) % terrain_width
			bness = self._brightnesses[bness_x]
			render_tile(p, light=bness)
			if p in gobj_cells:
				go = gobj_cells[p]
				to_draw = draw_graph.get_draws(go)
				for draw_gobj in to_draw:
					self._render_game_object(draw_gobj, light=bness)
					draw_graph.mark_drawn(draw_gobj)

	def highlight_tile(self, tile_p):
		"""
		Draws a green border around the tile at the given position.
		"""
		if not tile_p:
			return
		top = self.render_terrain.tile_top_polygon(tile_p)
		for p1_idx in range(4):
			p2_idx = (p1_idx + 1) % 4
			p1 = top[p1_idx]
			p2 = top[p2_idx]
			pygame.draw.line(self.window, HIGHLIGHT_COLOR, p1, p2)

	def highlight_tile_at_screen_pos(self, screen_pos):
		"""
		Highlights the tile at the given position.
		"""
		return self.highlight_tile(
			self.render_terrain.tile_at_screen_pos(screen_pos)
		)
