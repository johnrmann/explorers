import pygame
import math

from ..world.world import World
from src.render.viewport import Viewport
from src.render.utils import *
from src.math.map_range import map_range
from src.math.direction import *
from src.render.space import tile_to_screen_coords, screen_to_tile_coords

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

HIGHLIGHT_COLOR = (0, 250, 0)

def polygons(vp, terrain, tile):
	x,y = tile
	h = terrain.map[y][x]
	tx_screen, ty_screen = tile_to_screen_coords(tile, vp)
	bottom = tile_polygon(tx_screen, ty_screen, vp)
	top = height_offset_tile(bottom, h / 8, vp)
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
		lat_long = self.terrain.lat_long(p)
		bness = self.world.horology.brightness(self.world.utc, lat_long)
		bness2 = map_range(bness, (0, 1), (0.2, 1))
		top, left_wall, right_wall = polygons(self.vp, self.terrain, p)

		if top:
			color = scale_color(GROUND_COLOR, bness2)
			pygame.draw.polygon(self.window, color, top)

		should_render_left_wall = self.terrain.height_delta(
			p,
			left_wall_direction(self.vp.camera_orientation),
		)
		should_render_right_wall = self.terrain.height_delta(
			p,
			right_wall_direction(self.vp.camera_orientation),
		)
		if left_wall and should_render_left_wall:
			color = scale_color(WALL_COLOR_1, bness2)
			pygame.draw.polygon(self.window, color, left_wall)
		if right_wall and should_render_right_wall:
			color = scale_color(WALL_COLOR_2, bness2)
			pygame.draw.polygon(self.window, color, right_wall)

		should_render_left_ridge = self.terrain.height_delta(
			p,
			left_ridge_direction(self.vp.camera_orientation),
		)
		should_render_right_ridge = self.terrain.height_delta(
			p,
			right_ridge_direction(self.vp.camera_orientation)
		)
		if should_render_left_ridge:
			color = scale_color(WALL_COLOR_1, bness2)
			pygame.draw.line(self.window, color, top[3], top[0])
		if should_render_right_ridge:
			color = scale_color(WALL_COLOR_2, bness2)
			pygame.draw.line(self.window, color, top[0], top[1])

	def highlight_tile(self, p):
		top, _, _ = polygons(self.vp, self.terrain, p)
		for p1_idx in range(4):
			p2_idx = (p1_idx + 1) % 4
			p1 = top[p1_idx]
			p2 = top[p2_idx]
			pygame.draw.line(self.window, HIGHLIGHT_COLOR, p1, p2)
	
	def highlight_tile_at_screen_pos(self, screen_pos):
		x,y = screen_to_tile_coords(screen_pos, self.vp)
		p = (int(x), int(y))
		if x < 0 or y < 0:
			return
		if x >= self.terrain.width or y >= self.terrain.height:
			return
		self.highlight_tile(p)
