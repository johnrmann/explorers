import pygame

from src.math.map_range import map_range

from src.rendermath.order import cells_in_draw_order
from src.rendermath.draw_graph import DrawGraph
from src.rendermath.fit_rect import object_height_from_img_dims
from src.rendermath.box import Box

from src.world.world import World

from src.render.multisurface import MultiSurface, LIGHT_LEVELS
from src.render.viewport import Viewport
from src.render.render_terrain import RenderTerrain
from src.render.render_gameobject import render_gameobject

IMG_PATHS = [
	'assets/img/astronaut-cropped.png',
	'assets/img/lander.png',
	'assets/img/sprite/click-here.png',
	'assets/img/sprite/flag.png',
	'assets/img/sprite/palm-tree.png',
]

class Render:
	_last_zoom = 0

	_brightnesses = None

	def __init__(self, window, world: World, vp: Viewport, game_mgr=None):
		self.game_mgr = game_mgr
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = RenderTerrain(window, world, vp, self.game_mgr)
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
		self.draw_order = list(cells_in_draw_order(
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

	def _render_game_object(self, gobj, drawn_cells, light=None):
		# First, render all terrain tiles below the gobj.
		for p in gobj.cells_occupied(self.vp.camera_orientation):
			if p in drawn_cells:
				continue
			self.render_terrain.render_tile(p, light=light)
			drawn_cells.add(p)
		x, y = gobj.pos
		h = self.world.terrain.map[y][x]
		render_gameobject(
			window=self.window,
			clickmap=self.game_mgr.clickmap,
			vp=self.vp,
			go=gobj,
			height=h,
			image_map=self.images,
			light=light
		)

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
		if h == None:
			img_path = go.image_path()
			if img_path in self.image_z_factors:
				h = self.image_z_factors[img_path] * w
			else:
				h = 0
		return Box(p=pos, size=(w, d, h))

	def render(self):
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
		drawn = set()

		# Cache frequently accessed attributes and methods
		horology = self.world.horology
		render_tile = self.render_terrain.render_tile
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
			if p in drawn:
				continue
			bness_x = (x + time_offset) % terrain_width
			bness = self._brightnesses[bness_x]
			render_tile(p, light=bness)
			drawn.add(p)
			if p in gobj_cells:
				go = gobj_cells[p]
				to_draw = draw_graph.get_draws(go)
				for draw_gobj in to_draw:
					self._render_game_object(draw_gobj, drawn, light=bness)
					draw_graph.mark_drawn(draw_gobj)
