import pygame

from src.ctrl.camera import (
	pygame_key_to_delta_zoom,
	pygame_key_to_delta_camera_rotate,
	pygame_key_to_camdir
)

from src.ctrl.event_id import (
	EVENT_CAMERA_MOVE,
	EVENT_CAMERA_ZOOM,
	EVENT_CAMERA_ROTATE,
	EVENT_MOUSE_CLICK_WORLD,
)

class Control:
	"""
	Interprets pygame input and translates them into output via the event
	manager.
	"""

	evt_mgr = None
	game = None

	lock_camera: bool

	def __init__(self, lock_camera = False):
		from src.mgmt.singletons import get_event_manager, get_game_manager
		self.game = get_game_manager()
		self.evt_mgr = get_event_manager()
		self.lock_camera = lock_camera
	
	def interpret_pygame_camera_keyboard_event(self, event):
		d_camdir = pygame_key_to_camdir(event.key)
		d_zoom = pygame_key_to_delta_zoom(event.key)
		d_rotate = pygame_key_to_delta_camera_rotate(event.key)
		if d_camdir:
			self.evt_mgr.pub(EVENT_CAMERA_MOVE, data=d_camdir)
		if d_zoom:
			self.evt_mgr.pub(EVENT_CAMERA_ZOOM, data=d_zoom)
		if d_rotate:
			self.evt_mgr.pub(EVENT_CAMERA_ROTATE, data=d_rotate)
	
	def interpret_pygame_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.interpret_pygame_camera_keyboard_event(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			click_x, click_y = pygame.mouse.get_pos()
			self.evt_mgr.pub(
				EVENT_MOUSE_CLICK_WORLD, (click_x, click_y)
			)
	
	def interpret_pygame_input(self):
		for event in pygame.event.get():
			self.interpret_pygame_event(event)
