import pygame
import math
import numpy

from src.world.world import World
from src.world.terrain import Terrain
from src.render.viewport import ZOOMS, Viewport
from src.render.utils import *
from src.math.direction import *
from src.rendermath.tile import tile_polygon, is_point_in_tile, is_tile_in_screen
from src.rendermath.order import offset_tile_by_draw_order_vector
from src.rendermath.geometry import is_point_in_screen
from src.math.vector2 import Vector2
from src.render.render_tile import TileSurfaceCache

HIGHLIGHT_COLOR = (0, 250, 0)

class RenderTerrain(object):
	_ridge_draws: dict[int, dict[int, dict[Direction, int]]]

	terrain: Terrain

	def __init__(self, window, world: World, vp: Viewport, game_mgr=None):
		if game_mgr is None:
			from src.mgmt.singletons import get_game_manager
			self.game_mgr = get_game_manager()
		else:
			self.game_mgr = game_mgr
		self.world = world
		self.window = window
		self.vp = vp
		self.tile_cache = TileSurfaceCache()
		self.terrain = world.terrain
		self._calc_ridges()

	def _calc_ridge(self, cell_pos, direction: Direction):
		x, y = cell_pos
		left = self.terrain.height_delta(
			cell_pos, left_ridge_direction(direction)
		)
		right = self.terrain.height_delta(
			cell_pos, right_ridge_direction(direction)
		)
		left_bit = (left > 0) & 1
		right_bit = (right > 0) << 1
		self._ridge_draws[y][x][direction] = left_bit | right_bit

	def _calc_ridges(self):
		self._ridge_draws = {}
		for y in range(self.world.terrain.height):
			self._ridge_draws[y] = {}
			for x in range(self.world.terrain.width):
				self._ridge_draws[y][x] = {}
				for d in [Direction.NORTHWEST, Direction.NORTHEAST, Direction.SOUTHEAST, Direction.SOUTHWEST]:
					self._calc_ridge((x, y), d)

	def tile_bottom(self, tile_p):
		tile_screen = self.vp.tile_to_screen_coords(tile_p)
		return tile_polygon(tile_screen, self.vp.tile_dimensions)

	def tile_top(self, tile_p):
		x, y = tile_p
		if not 0 <= y < self.terrain.height:
			return None
		if not 0 <= x < self.terrain.width:
			return None
		h = self.terrain.map[y][x]
		bottom = self.tile_bottom(tile_p)
		return height_offset_tile(bottom, h / 8, self.vp)

	def tile_bottom_screen_coords(self, tile_p):
		tile_screen = self.vp.tile_to_screen_coords(tile_p)
		return tile_screen

	def tile_top_screen_coords(self, tile_p):
		bottom_screen_p = self.tile_bottom_screen_coords(tile_p)
		x, y = tile_p
		h = self.terrain.map[y][x % self.terrain.width]
		dy = h * self.vp.terrain_z
		bsp_x, bsp_y = bottom_screen_p
		return (bsp_x, bsp_y - dy)

	def render_tile(self, cell_p, light=7):
		x, y = cell_p
		if y < 0:
			return
		if y >= self.vp.terrain_height:
			return

		screen_p = self.tile_top_screen_coords(cell_p)
		zoom = self.vp.tile_width
		cam_ori = self.vp.camera_orientation

		ridges = self._ridge_draws[y][x % self.terrain.width][cam_ori]
		tile_surface, tile_pos = self.tile_cache.tile_surface_and_position(
			screen_p, zoom, ridges, light
		)
		self.window.blit(tile_surface, tile_surface.get_rect(topleft=tile_pos))

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
