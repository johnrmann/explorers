import pygame

from src.gameobject.actor import MoveActorEvent

from src.gui.action_menu import ActionMenu

from src.ctrl.camera import (
	pygame_key_to_delta_zoom,
	pygame_key_to_delta_camera_rotate,
	pygame_key_to_camdir
)
from src.ctrl.clickmap import ClickMap
from src.ctrl.event_id import (
	EVENT_CAMERA_MOVE,
	EVENT_CAMERA_ZOOM,
	EVENT_CAMERA_ROTATE,
	EVENT_MOUSE_CLICK_WORLD,
	EVENT_MOUSE_CLICK_OBJECT,
	CameraMoveEvent,
	CameraZoomEvent,
)

class Control:
	"""
	Interprets pygame input and translates them into output via the event
	manager.
	"""

	game_mgr = None
	clickmap: ClickMap

	lock_camera: bool

	def __init__(
			self,
			game_mgr,
			lock_camera = False,
			on_quit = None,
			clickmap = None
	):
		self.game_mgr = game_mgr
		self.clickmap = clickmap
		self.lock_camera = lock_camera
		self.on_quit = on_quit

	def interpret_pygame_camera_keyboard_event(self, event):
		d_camdir = pygame_key_to_camdir(event.key)
		d_zoom = pygame_key_to_delta_zoom(event.key)
		d_rotate = pygame_key_to_delta_camera_rotate(event.key)
		if d_camdir:
			self.game_mgr.evt_mgr.pub(CameraMoveEvent(d_camdir))
			return True
		if d_zoom:
			self.game_mgr.evt_mgr.pub(CameraZoomEvent(d_zoom))
			return True
		if d_rotate:
			# Rotation temporarily not supported - TODO(jm)
			return False
		return False

	def interpret_pygame_event(self, event):
		if event.type == pygame.QUIT and self.on_quit:
			self.on_quit()
			return True
		elif self.game_mgr.gui_mgr.process_event(event):
			return True
		elif event.type == pygame.KEYDOWN:
			self.interpret_pygame_camera_keyboard_event(event)
			return True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			click_x, click_y = pygame.mouse.get_pos()
			if not self.clickmap.is_terrain((click_x, click_y)):
				gobj = self.clickmap.game_object_at((click_x, click_y))
				# self.game_mgr.evt_mgr.pub(
				# 	EVENT_MOUSE_CLICK_OBJECT,
				# 	(gobj, (click_x, click_y))
				# )
				ActionMenu(
					origin=(click_x, click_y),
					clicked=gobj,
				)
				return True
			else:
				player_character = self.game_mgr.player_character
				click_tile = self.game_mgr.vp.screen_to_tile_coords((click_x, click_y))
				click_tile = (int(click_tile[0]), int(click_tile[1]))
				self.game_mgr.evt_mgr.pub(
					MoveActorEvent(
						actor=player_character,
						to_position=click_tile,
					)
				)
			return True
		return False

	def interpret_pygame_input(self):
		for event in pygame.event.get():
			if self.interpret_pygame_event(event):
				break
