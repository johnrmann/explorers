import math

from src.ctrl.event_id import (
	EVENT_CAMERA_MOVE,
	EVENT_CAMERA_ZOOM,
	EVENT_CAMERA_ROTATE,
	EVENT_MOUSE_CLICK_WORLD
)

from src.math.direction import (
	Direction,
	direction_to_delta,
	direction_rotate_90
)
from src.math.cart_prod import spatial_cart_prod
from src.mgmt.listener import Listener
from src.render.space import tile_screen_transform

TILE_WIDTH = 48
TILE_HEIGHT = TILE_WIDTH // 2

ZOOMS = [TILE_WIDTH / 4, TILE_WIDTH / 2, TILE_WIDTH, TILE_WIDTH * 2]

SAFETY = 3

class Viewport(Listener):
	_zoom_idx = 1

	camera_orientation = Direction.NORTHWEST

	def __init__(self, window_dims, terrain):
		from src.mgmt.singletons import get_event_manager
		self.evt_mgr = get_event_manager()
		self.window_dims = window_dims
		self.terrain_width, self.terrain_height = terrain.width, terrain.height
		self.camera_pos = terrain.center
		self.evt_mgr.sub(EVENT_CAMERA_MOVE, self)
		self.evt_mgr.sub(EVENT_CAMERA_ZOOM, self)
		self.evt_mgr.sub(EVENT_CAMERA_ROTATE, self)
		self.evt_mgr.sub(EVENT_MOUSE_CLICK_WORLD, self)
	
	def update(self, event_type, data):
		if event_type == EVENT_CAMERA_MOVE:
			self.move_camera(data)
		elif event_type == EVENT_CAMERA_ZOOM:
			self.change_zoom(data)
		elif event_type == EVENT_CAMERA_ROTATE:
			self.rotate_camera(data)
		elif event_type == EVENT_MOUSE_CLICK_WORLD:
			# TODO(jm) - i don't think this should go here, maybe explore a
			# mouse/screen interface class later?
			click_tile = self.screen_to_tile_coords(data)
			click_tile = (
				int(click_tile[0]), int(click_tile[1])
			)
			self.evt_mgr.pub("main.character.go", click_tile)
	
	@property
	def terrain_dims(self):
		return (self.terrain_width, self.terrain_height)

	@property
	def tile_width(self):
		return ZOOMS[self._zoom_idx]
	
	@property
	def tile_height(self):
		return self.tile_width / 2
	
	@property
	def tile_dimensions(self):
		return (self.tile_width, self.tile_height)

	@property
	def tile_z(self):
		w2 = (self.tile_width/2)**2
		h2 = (self.tile_height/2)**2
		return math.sqrt(w2 + h2)

	@property
	def terrain_z(self):
		return self.tile_z / 8
	
	def change_zoom(self, delta):
		if delta == 0:
			return
		self._zoom_idx = min(max(0, self._zoom_idx + delta), len(ZOOMS) - 1)

	def rotate_camera(self, delta):
		if delta == 0:
			return
		self.camera_orientation = direction_rotate_90(
			self.camera_orientation,
			quarter_turns=delta
		)
	
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

	def get_draw_points(self):
		xr = self.get_x_range()
		yr = self.get_y_range()
		if self.camera_orientation == Direction.NORTHWEST:
			return spatial_cart_prod(xr, yr)
		elif self.camera_orientation == Direction.NORTHEAST:
			return spatial_cart_prod(reversed(xr), yr)
		elif self.camera_orientation == Direction.SOUTHEAST:
			return spatial_cart_prod(reversed(xr), reversed(yr))
		elif self.camera_orientation == Direction.SOUTHWEST:
			return spatial_cart_prod(xr, reversed(yr))
		else:
			raise ValueError("Unknown camera orientation")
	
	def tile_to_screen_coords(self, p_tile):
		"""
		Converts tile coordinates to screen coordinates.
		"""
		win_width, win_height = self.window_dims
		cx_screen, cy_screen = self.global_tile_to_screen_coords(self.camera_pos)
		x2,y2 = self.global_tile_to_screen_coords(p_tile)
		return (
			x2 + (win_width // 2) - cx_screen,
			y2 + (win_height // 2) - cy_screen,
		)
	
	def global_tile_to_screen_coords(self, p):
		half_w = self.tile_width // 2
		half_h = self.tile_height // 2
		tx, ty = tile_screen_transform(p, self.camera_orientation)
		screen_x = tx * half_w
		screen_y = ty * half_h
		return (screen_x, screen_y)
	
	def screen_to_tile_coords(self, p_screen):
		"""
		Converts screen coordinates back into tile coordinates, considering
		camera orientation.
		"""
		screen_x, screen_y = p_screen
		win_width, win_height = self.window_dims
		s_cam_x, s_cam_y = self.global_tile_to_screen_coords(self.camera_pos)
		
		# Adjust the screen coordinates relative to the centered camera
		rel_screen_x = screen_x - (win_width // 2) + s_cam_x
		rel_screen_y = screen_y - (win_height // 2) + s_cam_y

		half_tw = self.tile_width // 2
		half_th = self.tile_height // 2
		
		# Apply the reverse transformation based on camera orientation
		if self.camera_orientation == Direction.NORTHWEST:
			# Default orientation
			x = (rel_screen_x // half_tw + rel_screen_y // half_th) // 2
			y = (rel_screen_y // half_th - rel_screen_x // half_tw) // 2
		elif self.camera_orientation == Direction.NORTHEAST:
			# 90-degree clockwise rotation
			x = (rel_screen_y // half_th - rel_screen_x // half_tw) // 2
			y = (rel_screen_y // half_th + rel_screen_x // half_tw) // 2
		elif self.camera_orientation == Direction.SOUTHEAST:
			# 180-degree rotation
			x = -(rel_screen_x // half_tw + rel_screen_y // half_th) // 2
			y = -(rel_screen_y // half_th - rel_screen_x // half_tw) // 2
		elif self.camera_orientation == Direction.SOUTHWEST:
			# 90-degree counterclockwise rotation
			x = (rel_screen_x // half_tw - rel_screen_y // half_th) // 2
			y = -(rel_screen_x // half_tw + rel_screen_y // half_th) // 2
		else:
			raise ValueError("Unsupported camera orientation")
		return (x, y)
