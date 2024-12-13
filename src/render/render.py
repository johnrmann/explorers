import pygame

from src.rendermath.order import cells_in_draw_order
from src.rendermath.draw_graph import DrawGraph

from src.world.world import World

from src.render.multisurface import MultiSurface
from src.render.viewport import Viewport
from src.render.render_terrain import RenderTerrain
from src.render.render_gameobject import render_gameobject

IMG_PATHS = [
	'assets/img/astronaut-cropped.png',
	'assets/img/lander.png',
	'assets/img/sprite/click-here.png',
	'assets/img/sprite/flag.png',
]

class Render(object):
	_last_zoom = 0

	def __init__(self, window, world: World, vp: Viewport, game_mgr=None):
		self.game_mgr = game_mgr
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = RenderTerrain(window, world, vp, self.game_mgr)
		self._load_images()
		self._calc_draw_order()
	
	def _load_images(self):
		self.images = {}
		for path in IMG_PATHS:
			surface = pygame.image.load(path).convert_alpha()
			multisurface = MultiSurface(
				surface,
				alpha_color=(255, 255, 255, 255),
				zoom_factors=[1.0]
			)
			self.images[path] = multisurface

	def _calc_draw_order(self):
		self._last_zoom = self.vp.tile_width
		self.draw_order = list(cells_in_draw_order(
			(0, 0),
			self.vp.camera_orientation,
			self.vp.tiles_wide,
			2 * self.vp.tiles_tall
		))

	def game_object_at(self, p):
		for go in self.game_mgr.game_objects:
			gx, gy = go.pos
			x, y = p
			if x == gx and y == gy:
				return go
		return None

	def _render_game_object(self, gobj, drawn_cells):
		# First, render all terrain tiles below the gobj.
		for p in gobj.cells_occupied(self.vp.camera_orientation):
			self.render_terrain.render_tile(p)
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
		)
	
	def render(self):
		if self.vp.tile_width != self._last_zoom:
			self._calc_draw_order()

		self.window.fill((0,0,200))

		pre_go_draw_graph = {
			go: go.bounding_box()
			for go in self.game_mgr.game_objects
		}
		draw_graph = DrawGraph(key_vals=pre_go_draw_graph)

		gobj_cells = {
			go.draw_point(self.vp.camera_orientation): go
			for go in self.game_mgr.game_objects
		}

		ox, oy = self.vp.get_draw_origin()
		drawn = set()

		for dx, dy in self.draw_order:
			x = ox + dx
			y = oy + dy
			p = (x, y)
			if p in drawn:
				continue
			self.render_terrain.render_tile(p)
			drawn.add(p)
			if p in gobj_cells:
				go = gobj_cells[p]
				to_draw = draw_graph.get_draws(go)
				for draw_gobj in to_draw:
					self._render_game_object(draw_gobj, drawn)
					draw_graph.mark_drawn(draw_gobj)
