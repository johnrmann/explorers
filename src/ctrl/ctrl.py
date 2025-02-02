import pygame

from src.gameobject.actor import MoveActorEvent, Actor

from src.gui.action_menu import ActionMenu
from src.gui.playbar import PlaybarMode

from src.debug.debug import command_to_event

from src.ctrl.camera import (
	pygame_key_to_delta_zoom,
	pygame_key_to_delta_camera_rotate,
	pygame_key_to_camdir
)
from src.ctrl.clickmap import ClickMap
from src.ctrl.event_id import (
	CameraMoveEvent,
	CameraZoomEvent,
)

class Control:
	"""
	Interprets pygame input and translates them into output via the event
	manager.
	"""

	# TODO(jm)
	_player_id: int = 1

	game_mgr = None
	clickmap: ClickMap

	lock_camera: bool

	_screen_to_tile = None
	cell_under_mouse = None

	_playbar_mode: PlaybarMode = PlaybarMode.CHARACTER
	selected_game_object = None
	build_object_prototype = None

	def __init__(
			self,
			game_mgr,
			lock_camera = False,
			on_quit = None,
			clickmap = None,
			screen_to_tile = None,
			get_mouse_pos = None,
	):
		self.game_mgr = game_mgr
		self.clickmap = clickmap
		self.lock_camera = lock_camera
		self.on_quit = on_quit
		self._screen_to_tile = screen_to_tile
		if get_mouse_pos is None:
			self._get_mouse_pos = pygame.mouse.get_pos
		else:
			self._get_mouse_pos = get_mouse_pos


	def tick(self, dt: float):
		"""
		Called once per frame to update the mouse position and the selected
		game object position.
		"""
		mouse_x, mouse_y = self._get_mouse_pos()
		if self._screen_to_tile:
			new_cell_under_mouse = self._screen_to_tile((mouse_x, mouse_y))
			if new_cell_under_mouse is not None:
				self.cell_under_mouse = new_cell_under_mouse
			selected_game_object = self.selected_game_object
			if self._can_move_game_objects and selected_game_object:
				can_move = selected_game_object.is_moveable(self._player_id)
				if can_move:
					selected_game_object.pos = self.cell_under_mouse


	@property
	def _can_move_game_objects(self):
		return self._playbar_mode == PlaybarMode.BUILD


	def playbar_mode_changed(self, new_mode: PlaybarMode):
		"""
		Called whenever the playbar mode changes. When we go into build mode,
		disable character movement and allow for clicking and dragging
		game objects.
		"""
		self._playbar_mode = new_mode
		if new_mode != PlaybarMode.BUILD:
			if self.build_object_prototype:
				self._cancel_placing_new_game_object()
			else:
				self._place_moving_game_object()
			self.build_object_prototype = None


	def _place_moving_game_object(self):
		if self.selected_game_object:
			self.selected_game_object.pos = self.cell_under_mouse
			self.selected_game_object = None


	def _cancel_placing_new_game_object(self):
		if self.selected_game_object and self.build_object_prototype:
			self.game_mgr.remove_game_object(self.selected_game_object)
			self.selected_game_object = None
			self.build_object_prototype = None


	def _new_game_object_from_prototype(self):
		if self.build_object_prototype:
			self.selected_game_object = self.build_object_prototype.make()
			self.selected_game_object.pos = self.cell_under_mouse
			self.game_mgr.add_game_object(self.selected_game_object)


	def playbar_selected_build_object(self, build_object_prototype):
		if self._playbar_mode != PlaybarMode.BUILD:
			return
		self.build_object_prototype = build_object_prototype
		self._new_game_object_from_prototype()


	def playbar_deselected_build_object(self):
		if self._playbar_mode != PlaybarMode.BUILD:
			return
		if self.selected_game_object:
			self.game_mgr.remove_game_object(self.selected_game_object)
		self.selected_game_object = None
		self.build_object_prototype = None


	def _interpret_debug_console_command(self, event):
		key = event.key
		if key == pygame.K_BACKQUOTE:
			command = input("Debug command: ")
			if command:
				event = command_to_event(command)
				if event:
					self.game_mgr.evt_mgr.pub(event)


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


	def _interpret_character_mode_click_event(self):
		click_x, click_y = self._get_mouse_pos()
		if not self.clickmap.is_terrain((click_x, click_y)):
			gobj = self.clickmap.game_object_at((click_x, click_y))
			if isinstance(gobj, Actor) and gobj.owner == self._player_id:
				self.game_mgr.selected_actor = gobj
			else:
				ActionMenu(
					origin=(click_x, click_y),
					clicked=gobj,
				)
			return True
		else:
			selected_actor = self.game_mgr.selected_actor
			self.game_mgr.evt_mgr.pub(
				MoveActorEvent(
					actor=selected_actor,
					to_position=self.cell_under_mouse,
				)
			)
		return True


	def _interpret_build_mode_key_event(self, event):
		if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
			moving_gobj = self.selected_game_object
			if moving_gobj and moving_gobj.is_deleteable(self._player_id):
				self.game_mgr.remove_game_object(self.selected_game_object)
				self.selected_game_object = None
				return True
		
		if event.key == pygame.K_ESCAPE:
			if self.selected_game_object and self.build_object_prototype:
				self._cancel_placing_new_game_object()
				return True

		return False


	def _interpret_build_mode_click_event(self):
		click_pos = self._get_mouse_pos()
		clicked_terrain = self.clickmap.is_terrain(click_pos)

		# Try to pick up an existing game object.
		if not self.selected_game_object and not clicked_terrain:
			gobj = self.clickmap.game_object_at(click_pos)
			if gobj and gobj.is_selectable(self._player_id):
				self.selected_game_object = gobj
				return True

		# Place a new game object.
		elif self.selected_game_object and self.build_object_prototype:
			self._place_moving_game_object()
			self._new_game_object_from_prototype()
			return True

		# Place an existing game object.
		elif self.selected_game_object and not self.build_object_prototype:
			self._place_moving_game_object()
			return True

		return False


	def interpret_pygame_event(self, event):
		if event.type == pygame.QUIT and self.on_quit:
			self.on_quit()
			return True
		elif self.game_mgr.gui_mgr.process_event(event):
			return True
		elif event.type == pygame.KEYDOWN:
			self._interpret_debug_console_command(event)
			self.interpret_pygame_camera_keyboard_event(event)
			if self._playbar_mode == PlaybarMode.BUILD:
				self._interpret_build_mode_key_event(event)
			return True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if self._playbar_mode == PlaybarMode.BUILD:
				return self._interpret_build_mode_click_event()
			elif self._playbar_mode == PlaybarMode.CHARACTER:
				return self._interpret_character_mode_click_event()
		return False


	def interpret_pygame_input(self):
		for event in pygame.event.get():
			if self.interpret_pygame_event(event):
				break
