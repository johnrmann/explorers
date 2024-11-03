import pygame

from src.world.world import World
from src.render.viewport import Viewport
from src.render.render_terrain import RenderTerrain
from src.render.render_gameobject import render_gameobject

class Render(object):
	def __init__(self, window, world: World, vp: Viewport):
		self.window = window
		self.world = world
		self.vp = vp
		self.render_terrain = RenderTerrain(window, world, vp)
		self._load_images()
	
	def _load_images(self):
		self.images = {}
		self.images['assets/img/astronaut-cropped.png'] = pygame.image.load('assets/img/astronaut-cropped.png')
	
	def game_object_at(self, p):
		for go in self.world.game_objects:
			gx, gy = go.pos
			x, y = p
			if x == gx and y == gy:
				return go
		return None
	
	def render(self):
		self.window.fill((0,0,200))
		for p in self.vp.get_draw_points():
			(x,y) = p
			self.render_terrain.render_tile(p)
			if self.game_object_at(p):
				h = self.world.terrain.map[y][x]
				render_gameobject(
					window=self.window,
					vp=self.vp,
					go=self.game_object_at(p),
					height=h,
					image_map=self.images
				)
