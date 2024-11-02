import math
import pygame

from src.math.direction import Direction, direction_to_delta

TILE_WIDTH = 48
TILE_HEIGHT = TILE_WIDTH // 2

ZOOMS = [TILE_WIDTH / 4, TILE_WIDTH / 2, TILE_WIDTH, TILE_WIDTH * 2]

SAFETY = 3

def pygame_key_to_delta_zoom(key):
	"""
	Converts a key press to whether we should zoom in or zoom out.
	"""
	if key == pygame.K_KP_PLUS or key == pygame.K_PLUS:
		return 1
	elif key == pygame.K_KP_MINUS or key == pygame.K_MINUS:
		return -1
	return 0

def pygame_key_to_camdir(key):
	"""
	Converts a key press to which direction the camera should move.
	"""
	if key == pygame.K_UP:
		return Direction.NORTHWEST
	elif key == pygame.K_DOWN:
		return Direction.SOUTHEAST
	elif key == pygame.K_RIGHT:
		return Direction.NORTHEAST
	elif key == pygame.K_LEFT:
		return Direction.SOUTHWEST
	return None

class Viewport(object):
	_zoom_idx = 1

	camera_orientation = Direction.NORTHWEST

	def __init__(self, window_dims, terrain):
		self.window_dims = window_dims
		self.terrain_width, self.terrain_height = terrain.width, terrain.height
		self.camera_pos = terrain.center
	
	@property
	def tile_width(self):
		return ZOOMS[self._zoom_idx]
	
	@property
	def tile_height(self):
		return self.tile_width / 2

	@property
	def tile_z(self):
		w2 = (self.tile_width/2)**2
		h2 = (self.tile_height/2)**2
		return math.sqrt(w2 + h2)

	@property
	def terrain_z(self):
		return self.tile_z / 8
	
	def change_zoom(self, delta):
		self._zoom_idx = min(max(0, self._zoom_idx + delta), len(ZOOMS) - 1)
	
	def move_camera(self, camdir: Direction):
		if not camdir:
			return

		dx,dy = direction_to_delta(camdir)
		cx,cy = self.camera_pos
		cx2,cy2 = (cx + dx, cy + dy)

		if cy2 < 0:
			cy2 = 0
		elif cy2 >= self.terrain_height:
			cy2 = self.terrain_height - 1
		
		if cx2 == -1:
			cx2 = self.terrain_width - 1
		if cx2 >= self.terrain_width:
			cx2 = 0
		
		self.camera_pos = (cx2, cy2)
	
	def get_x_range(self):
		win_width, _ = self.window_dims
		cx, _ = self.camera_pos
		left = max(
			0,
			math.ceil(cx - (win_width / self.tile_width)) - SAFETY
		)
		right = min(
			self.terrain_width,
			math.ceil(cx + (win_width / self.tile_width)) + SAFETY
		)
		return range(left, right)
	
	def get_y_range(self):
		_, win_height = self.window_dims
		_, cy = self.camera_pos
		top = max(
			0,
			math.ceil(cy - (win_height / self.tile_height)) - SAFETY
		)
		bottom = min(
			self.terrain_height,
			math.ceil(cy + (win_height / self.tile_height)) + SAFETY
		)
		return range(top, bottom)
	