import pygame

from src.rendermath.order import cells_in_draw_order
from src.rendermath.draw_graph import DrawGraph

from src.world.world import World
from src.render.viewport import Viewport
from src.render.render_terrain import RenderTerrain
from src.render.render_gameobject import render_gameobject

class Render(object):
	def __init__(self, window, world: World, vp: Viewport):
		from src.mgmt.singletons import get_game_manager
		self.game_mgr = get_game_manager()
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = RenderTerrain(window, world, vp)
		self._load_images()
	
	def _load_images(self):
		self.images = {}
		self.images['assets/img/astronaut-cropped.png'] = pygame.image.load('assets/img/astronaut-cropped.png')
		self.images['assets/img/lander.png'] = pygame.image.load('assets/img/lander.png')
		self.images['assets/img/sprite/click-here.png'] = pygame.image.load('assets/img/sprite/click-here.png')
		self.images['assets/img/sprite/flag.png'] = pygame.image.load('assets/img/sprite/flag.png')
	
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
			vp=self.vp,
			go=gobj,
			height=h,
			image_map=self.images
		)
	
	def render(self):
		self.window.fill((0,0,200))

		pre_go_draw_graph = {}
		for go in self.game_mgr.game_objects:
			pre_go_draw_graph[go] = go.bounding_box()
		draw_graph = DrawGraph(key_vals=pre_go_draw_graph)

		gobj_cells = {}
		for go in self.game_mgr.game_objects:
			gobj_cells[go.draw_point(self.vp.camera_orientation)] = go

		origin_cell = self.vp.get_draw_origin()
		cells = list(cells_in_draw_order(
			origin_cell,
			self.vp.camera_orientation,
			self.vp.tiles_wide,
			2 * self.vp.tiles_tall
		))
		drawn = set()

		for p in cells:
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
