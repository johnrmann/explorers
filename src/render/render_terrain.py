import pygame
import math

from ..world.world import World
from src.render.viewport import Viewport
from src.render.utils import *

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

def polygons(vp, terrain, tile):
	x,y = tile
	h = terrain.map[y][x]
	tx_screen, ty_screen = tile_coords_to_screen_coords(tile, vp)
	bottom = tile_polygon(tx_screen, ty_screen, vp)
	top = height_offset_tile(bottom, h, vp)
	return box_between_tiles(top, bottom)

class RenderTerrain(object):
	def __init__(self, window, world: World, vp: Viewport):
		self.world = world
		self.window = window
		self.vp = vp
	
	@property
	def terrain(self):
		return self.world.terrain

	def render_tile(self, p):
		latLong = self.terrain.latLong(p)
		bness = self.world.horology.brightness(self.world.utc, latLong)
		top, left_wall, right_wall = polygons(self.vp, self.terrain, p)
		if top:
			color = scale_color(GROUND_COLOR, bness)
			pygame.draw.polygon(self.window, color, top)
		if left_wall:
			color = scale_color(WALL_COLOR_1, bness)
			pygame.draw.polygon(self.window, color, left_wall)
		if right_wall:
			color = scale_color(WALL_COLOR_2, bness)
			pygame.draw.polygon(self.window, color, right_wall)
