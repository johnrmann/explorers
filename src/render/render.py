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
	
	def game_object_at(self, p):
		for go in self.world.game_objects:
			gx, gy = go.pos
			x, y = p
			if x == gx and y == gy:
				return go
		return None
	
	def render(self):
		self.window.fill((0,0,200))
		for x in self.vp.get_x_range():
			for y in self.vp.get_y_range():
				p = (x,y)
				self.render_terrain.render_tile(p)
				if self.game_object_at(p):
					h = self.world.terrain.map[y][x]
					render_gameobject(self.window, self.vp, self.game_object_at(p), h)
