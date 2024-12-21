import pygame

from typing import final

from src.mgmt.event_manager import EventManager

from src.gui.anchor import Anchor, origin_via_anchor

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
		"""Draws all GUI elements on the screen."""
		for elem in self.elements:
			if not elem.hidden:
				elem.draw(screen)

_global_gui_manager = None

def init_gui_manager(game_mgr):
	global _global_gui_manager
	_global_gui_manager = _GuiManager(game_mgr=game_mgr)
	return _global_gui_manager

class GuiElement:
	"""
	All GUI Elements have an origin, dimensions, and a connection to the GUI
	Manager. They optionally have a parent and list of children.
	"""

	gui_mgr: _GuiManager
	evt_mgr: EventManager

	hidden = False

	parent = None
	elements = None

	relative_origin: tuple[int, int] = None
	dimensions: tuple[int, int] = None
	anchor: Anchor

	def __init__(
			self,
			parent=None,
			hidden=False,
			rect = None, origin=None, dimensions=None, anchor=None,
			gui_mgr=None, evt_mgr=None
	):
		self.hidden = hidden
		self.elements = []
		self.anchor = anchor
		if rect is not None:
			origin, dimensions = rect
		if dimensions is not None:
			self.dimensions = dimensions
		if origin is not None:
			self.relative_origin = origin
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
	def _parent_origin(self):
		"""The origin of the parent element."""
		if self.parent is not None:
			return self.parent.origin
		return (0, 0)

	@property
	def _parent_dimensions(self):
		"""The dimensions of the parent element."""
		if self.parent is not None:
			return self.parent.dimensions
		return self.gui_mgr.surface.get_size()

	@property
	def origin(self):
		"""The absolute origin of the element."""
		if self.relative_origin is None:
			raise ValueError("No origin set.")
		if self.anchor is not None:
			return origin_via_anchor(
				self.relative_origin,
				self.dimensions,
				self._parent_dimensions,
				anchor=self.anchor,
				parent_origin=self._parent_origin
			)
		rx, ry = self.relative_origin
		if self.parent is not None:
			px, py = self.parent.origin
			return px + rx, py + ry
		return rx, ry

	@property
	def pygame_rect(self):
		"""The absolute origin and dimensions of the element."""
		if self.dimensions is None:
			raise ValueError("No dimensions set.")
		ox, oy = self.origin
		w, h = self.dimensions
		return pygame.Rect(ox, oy, w, h)

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
		if self.hidden:
			return False
		for child in self.elements:
			if not child.hidden and child.process_event(event):
				return True
		return self.my_process_event(event)

	def my_process_event(self, event):
		"""Processes the event for this element."""
		return False

	@final
	def update(self, dt: float):
		"""Updates the GUI element."""
		if self.hidden:
			return
		self.my_update(dt)
		for elem in self.elements:
			if not elem.hidden:
				elem.update(dt)

	def my_update(self, dt: float):
		"""Updates the GUI element."""
		return

	@final
	def draw(self, screen):
		"""
		Draws this element and its children on the screen. Do not override -
		all actual rendering should be done in the _draw method.
		"""
		if self.hidden:
			return
		self.my_draw(screen)
		for elem in self.elements:
			if not elem.hidden:
				elem.draw(screen)

	def my_draw(self, screen):
		"""Draws the element on the screen."""
		return
