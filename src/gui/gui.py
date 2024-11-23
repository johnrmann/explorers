import pygame
from src.mgmt.event_manager import EventManager

class _GuiManager:
	elements = []

	game_mgr = None

	def __init__(self, game_mgr=None):
		if game_mgr is None:
			raise ValueError("Game manager must be provided.")
		self.game_mgr = game_mgr
		self.surface = pygame.display.get_surface()
		if not self.surface:
			raise ValueError("pygame not initialized yet")

	def remove_element(self, element):
		"""Removes the given element from being rendered."""
		if element in self.elements:
			self.elements.remove(element)

	def process_event(self, event):
		for elem in self.elements:
			if elem.process_event(event):
				return True
		return False

	def update(self, dt: float):
		for elem in self.elements:
			elem.update(dt)

	def draw(self, screen):
		for elem in self.elements:
			elem.draw(screen)

_global_gui_manager = None

def init_gui_manager(game_mgr):
	global _global_gui_manager
	_global_gui_manager = _GuiManager(game_mgr=game_mgr)
	return _global_gui_manager

class GuiElement:
	gui_mgr: _GuiManager
	evt_mgr: EventManager

	parent = None
	elements = None

	relative_origin: tuple[int, int]
	dimensions: tuple[int, int]

	def __init__(self, gui_mgr=None, parent=None, evt_mgr=None):
		self.elements = []
		if gui_mgr is not None:
			self.gui_mgr = gui_mgr
		else:
			self.gui_mgr = _global_gui_manager
		if evt_mgr is not None:
			self.evt_mgr = evt_mgr
		else:
			self.evt_mgr = self.gui_mgr.game_mgr.evt_mgr
		if parent is not None:
			self.parent = parent
			self.parent.add_child(self)
		else:
			self.gui_mgr.elements.append(self)

	def __del__(self):
		self.remove_me()

	def remove_me(self):
		"""
		Removes this element from the GUI manager.
		"""
		if self.parent is not None:
			self.parent.remove_child(self)
			self.parent = None
		else:
			self.gui_mgr.remove_element(self)

	@property
	def origin(self):
		rx, ry = self.relative_origin
		if self.parent is not None:
			px, py = self.parent.origin
			return px + rx, py + ry
		return rx, ry

	def add_child(self, child):
		"""Adds a child element to this element."""
		self.elements.append(child)
		child.parent = self

	def remove_child(self, child):
		"""Removes a child element."""
		if child in self.elements:
			self.elements.remove(child)
			child.parent = None
			del child

	def process_event(self, event):
		"""Returns true if the event was for this controller."""
		for child in self.elements:
			if child.process_event(event):
				return True
		return False

	def update(self, dt: float):
		"""Updates the GUI element."""
		pass

	def draw(self, screen):
		"""Draws the element on the screen."""
		for elem in self.elements:
			elem.draw(screen)

class GuiPrimitive(GuiElement):
	"""
	To be extended by the various GUI controls to be shown on the screen.
	"""

	def __init__(self, rect=None, parent=None, evt_mgr=None):
		if rect is None:
			raise ValueError("Every GUI element must have a rect.")
		origin, dimensions = rect
		self.relative_origin = origin
		self.dimensions = dimensions
		super().__init__(parent=parent, evt_mgr=evt_mgr)

	@property
	def screen_dimensions(self):
		"""The dimensions of the screen."""
		return self.gui_mgr.surface.get_size()

	@property
	def pygame_rect(self):
		ox, oy = self.origin
		w, h = self.dimensions
		return pygame.Rect(ox, oy, w, h)
