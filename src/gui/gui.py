import pygame

class _GuiManager:
	elements = []

	def __init__(self):
		self.surface = pygame.display.get_surface()
		if not self.surface:
			raise ValueError("pygame not initialized yet")

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

def init_gui_manager():
	global _global_gui_manager
	_global_gui_manager = _GuiManager()
	return _global_gui_manager

class GuiElement:
	gui_mgr: _GuiManager
	parent = None
	elements = []

	def __init__(self, parent=None):
		self.gui_mgr = _global_gui_manager
		if parent is not None:
			self.parent = parent
			self.parent.elements.append(self)
		else:
			self.gui_mgr.elements.append(self)

	def __del__(self):
		if self in self.gui_mgr.elements:
			self.gui_mgr.elements.remove(self)

	def process_event(self, event):
		"""Returns true if the event was for this controller."""
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

	def __init__(self, rect=None, parent=None):
		super().__init__(parent=parent)
		if rect is None:
			raise ValueError("Every GUI element must have a rect.")
		origin, dimensions = rect
		self.relative_origin = origin
		self.dimensions = dimensions

	@property
	def screen_dimensions(self):
		"""The dimensions of the screen."""
		return self.gui_mgr.surface.get_size()

	@property
	def origin(self):
		if self.parent is None:
			return self.relative_origin
		else:
			pox, poy = self.parent.origin
			x, y = self.relative_origin
			return (pox + x, poy + y)

	@property
	def pygame_rect(self):
		ox, oy = self.origin
		w, h = self.dimensions
		return pygame.Rect(ox, oy, w, h)
