import math

from src.ctrl.event_id import (
	CameraMoveEvent,
	CameraZoomEvent,
	CameraRotateEvent,
)

from src.math.direction import (
	Direction,
	direction_to_delta,
	direction_rotate_90,
	left_wall_direction,
	right_wall_direction,
	left_ridge_direction,
	right_ridge_direction,
	quarter_turns_between_directions,
)
from src.math.vector2 import vector2_rotate_point
from src.mgmt.listener import Listener
from src.rendermath.cell import cell_position_on_global_screen
from src.rendermath.tile import tile_z_for_width
from src.rendermath.terrain import TERRAIN_STEPS_PER_CELL

TILE_WIDTH = 64
TILE_HEIGHT = TILE_WIDTH // 2
TILE_THICKNESS = TILE_WIDTH // 2

ZOOMS = [TILE_WIDTH // 4, TILE_WIDTH // 2, TILE_WIDTH, TILE_WIDTH * 2]

SAFETY = 3

class Viewport(Listener):
	_zoom_idx = 1
	_camera_pos = (0, 0)
	_camera_screen_pos = (0, 0)
	_camera_screen_transform = (0, 0)

	camera_orientation = Direction.NORTHWEST

	left_wall_direction = left_wall_direction(Direction.NORTHWEST)
	right_wall_direction = right_wall_direction(Direction.NORTHWEST)
	left_ridge_direction = left_ridge_direction(Direction.NORTHWEST)
	right_ridge_direction = right_ridge_direction(Direction.NORTHWEST)

	_game_mgr = None
	evt_mgr = None

	def __init__(self, window_dims, terrain):
		self.window_dims = window_dims
		self.terrain_width, self.terrain_height = terrain.width, terrain.height
		self.terrain_dims = (self.terrain_width, self.terrain_height)
		self._camera_pos = terrain.center
		self._recompute_tile_dimensions()
		self._recompute_screen_dimensions()
		self._recompute_camera()

	def _recompute_camera(self):
		self._camera_screen_pos = self.cell_position_on_global_screen(
			self.camera_pos
		)
		self._camera_screen_transform = (
			(self.window_dims[0] // 2) - self._camera_screen_pos[0],
			(self.window_dims[1] // 2) - self._camera_screen_pos[1]
		)

	def _recompute_tile_dimensions(self):
		self.tile_width = ZOOMS[self._zoom_idx]
		self.tile_height = self.tile_width // 2
		self.tile_z = tile_z_for_width(self.tile_width)
		self.tile_dimensions = (self.tile_width, self.tile_height)
		self.terrain_z = self.tile_z / TERRAIN_STEPS_PER_CELL

	def _subscribe_to_events(self):
		self.evt_mgr.sub('CameraMoveEvent', self)
		self.evt_mgr.sub('CameraZoomEvent', self)
		self.evt_mgr.sub('CameraRotateEvent', self)

	@property
	def camera_pos(self):
		"""The camera position."""
		return self._camera_pos

	@camera_pos.setter
	def camera_pos(self, value):
		self._camera_pos = value
		self._recompute_camera()

	@property
	def game_mgr(self):
		return self._game_mgr

	@game_mgr.setter
	def game_mgr(self, value):
		if self._game_mgr is not None:
			raise ValueError("Write-once property.")
		self._game_mgr = value
		self.evt_mgr = value.evt_mgr
		self._subscribe_to_events()

	def update(self, event):
		if isinstance(event, CameraMoveEvent):
			self.move_camera(event.direction)
		elif isinstance(event, CameraZoomEvent):
			self.change_zoom(event.delta)
		elif isinstance(event, CameraRotateEvent):
			self.rotate_camera(event.delta)

	def change_zoom(self, delta):
		if delta == 0:
			return
		self._zoom_idx = min(max(0, self._zoom_idx + delta), len(ZOOMS) - 1)
		self._recompute_tile_dimensions()
		self._recompute_screen_dimensions()
		self._recompute_camera()

	def _recompute_screen_dimensions(self):
		win_w, win_h = self.window_dims
		self.tiles_wide = int(win_w // self.tile_width) + 2
		self.tiles_tall = 2 * int(win_h // self.tile_height) + 2

	def _update_walls_and_ridges(self):
		co = self.camera_orientation
		self.left_wall_direction = left_wall_direction(co)
		self.right_wall_direction = right_wall_direction(co)
		self.left_ridge_direction = left_ridge_direction(co)
		self.right_ridge_direction = right_ridge_direction(co)

	def rotate_camera(self, delta):
		if delta == 0:
			return
		self.camera_orientation = direction_rotate_90(
			self.camera_orientation,
			quarter_turns=delta
		)
		self._update_walls_and_ridges()
		self._recompute_camera()

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
		self._recompute_camera()

	def get_draw_origin(self):
		x, y = self.camera_pos
		dir_diff = quarter_turns_between_directions(
			Direction.NORTHWEST, self.camera_orientation
		)
		dx = -((self.tiles_tall // 2) + (self.tiles_wide // 2))
		dy = -((self.tiles_tall // 2) - (self.tiles_wide // 2))
		dx, dy = vector2_rotate_point((dx, dy), dir_diff)
		return (x + dx, y + dy)

	def tile_to_screen_coords(self, p_tile):
		"""
		Converts tile coordinates to screen coordinates.
		"""
		tx, ty = self._camera_screen_transform
		x2,y2 = self.cell_position_on_global_screen(p_tile)
		return (
			x2 + tx,
			y2 + ty,
		)

	def global_screen_position_to_screen_position(self, position):
		"""
		Converts a global screen position to a screen position.
		"""
		tx, ty = self._camera_screen_transform
		x, y = position
		return (x + tx, y + ty)

	def cell_position_on_global_screen(self, cell_pos):
		"""
		Convenience wrapper for cell_position_on_global_screen.
		"""
		return cell_position_on_global_screen(
			cell_pos,
			self.camera_orientation,
			self.tile_dimensions
		)

	def screen_to_tile_coords(self, p_screen):
		"""
		Converts screen coordinates back into tile coordinates, considering
		camera orientation.
		"""
		screen_x, screen_y = p_screen
		win_width, win_height = self.window_dims
		s_cam_x, s_cam_y = self._camera_screen_pos

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
