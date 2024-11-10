import pygame
import math

from ..world.world import World
from src.render.viewport import Viewport
from src.render.utils import *
from src.math.map_range import map_range
from src.math.direction import *
from src.rendermath.tile import tile_polygon, is_point_in_tile, is_tile_in_screen
from src.rendermath.order import offset_tile_by_draw_order_vector
from src.rendermath.geometry import is_point_in_screen
from src.math.vector2 import Vector2

GROUND_COLOR = (200, 0, 0)
WALL_COLOR_1 = (100, 0, 0)
WALL_COLOR_2 = (50, 0, 0)

HIGHLIGHT_COLOR = (0, 250, 0)

# TODO(jm) - how to inject this
SCREEN_DIMS = Vector2(1440, 900)

def polygons(vp: Viewport, terrain, tile):
	x,y = tile
	h = terrain.map[y][x]
	tile_screen = vp.tile_to_screen_coords(tile)
	bottom = tile_polygon(tile_screen, vp.tile_dimensions)
	top = height_offset_tile(bottom, h / 8, vp)
	return box_between_tiles(top, bottom)

class RenderTerrain(object):
	def __init__(self, window, world: World, vp: Viewport):
		from src.mgmt.singletons import get_game_manager
		self.game = get_game_manager()
		self.world = world
		self.window = window
		self.vp = vp
	
	@property
	def terrain(self):
		return self.world.terrain

	def tile_bottom(self, tile_p):
		tile_screen = self.vp.tile_to_screen_coords(tile_p)
		return tile_polygon(tile_screen, self.vp.tile_dimensions)

	def tile_top(self, tile_p):
		x, y = tile_p
		if not 0 <= y < self.terrain.height:
			return None
		h = self.terrain.map[y][x]
		bottom = self.tile_bottom(tile_p)
		return height_offset_tile(bottom, h / 8, self.vp)

	def render_tile(self, p):
		lat_long = self.terrain.lat_long(p)
		bness = self.world.horology.brightness(self.game.utc, lat_long)
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

	def tile_at_screen_pos(self, screen_p):
		"""
		Returns the tile at the current mouse cursor position.
		"""
		if not is_point_in_screen(screen_p, self.vp.window_dims):
			return None
		x, y = self.vp.screen_to_tile_coords(screen_p)
		original = Vector2(x, y).round()
		max_h = -1
		found = None
		for direction in [-1, 1]:
			k = 0
			while True:
				p_left, p_right = offset_tile_by_draw_order_vector(
					original,
					self.vp.camera_orientation,
					k * direction
				)
				t_left = self.tile_top(p_left)
				t_right = self.tile_top(p_right)
				if not t_left and not t_right:
					break
				win_dims = self.vp.window_dims
				l_in_screen = t_left and is_tile_in_screen(t_left, win_dims)
				r_in_screen = t_right and is_tile_in_screen(t_right, win_dims)
				if not l_in_screen and not r_in_screen:
					break
				if t_left and is_point_in_tile(screen_p, t_left):
					h_left = self.terrain.height_at(p_left)
					if h_left > max_h:
						max_h = h_left
						found = p_left
				elif t_right and is_point_in_tile(screen_p, t_right):
					h_right = self.terrain.height_at(p_right)
					if h_right > max_h:
						max_h = h_right
						found = p_right
				k += 1
		return found

	def highlight_tile(self, tile_p):
		"""
		Draws a green border around the tile at the given position.
		"""
		if not tile_p:
			return
		top = self.tile_top(tile_p)
		for p1_idx in range(4):
			p2_idx = (p1_idx + 1) % 4
			p1 = top[p1_idx]
			p2 = top[p2_idx]
			pygame.draw.line(self.window, HIGHLIGHT_COLOR, p1, p2)

	def highlight_tile_at_screen_pos(self, screen_pos):
		"""
		Highlights the tile at the given position.
		"""
		return self.highlight_tile(self.tile_at_screen_pos(screen_pos))
