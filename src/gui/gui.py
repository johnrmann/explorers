import pygame
import pygame_gui

class _GuiManager:
	elements = set()
	element_to_callback = {}

	def __init__(self):
		self.surface = pygame.display.get_surface()
		if not self.surface:
			raise ValueError("pygame not initialized yet")
		self.manager = pygame_gui.UIManager(self.surface.get_size())

	def process_events(self, event):
		self.manager.process_events(event)
		if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
			clicked = self.element_to_callback.get(event.ui_element)
			if clicked:
				clicked()
				return True
		return False

	def update(self, dt: float):
		self.manager.update(dt)
		for elem in self.elements:
			elem.update(dt)

	def draw_ui(self):
		self.manager.draw_ui(self.surface)

_global_gui_manager = None

def init_gui_manager():
	global _global_gui_manager
	_global_gui_manager = _GuiManager()
	return _global_gui_manager

class GuiElement:
	"""
	To be extended by the various GUI controls to be shown on the screen.
	"""

	gui_mgr: _GuiManager

	def __init__(self):
		self.gui_mgr = _global_gui_manager
		self.gui_mgr.elements.add(self)

	def __del__(self):
		self.gui_mgr.elements.remove(self)

	@property
	def screen_dimensions(self):
		"""The dimensions of the screen."""
		return self.gui_mgr.surface.get_size()

	@property
	def pygame_manager(self):
		"""Return the pygame GUI manager."""
		return self.gui_mgr.manager

	@property
	def pygame_container(self):
		"""Return the pygame element that we are wrapping."""
		return None

	def update(self, dt: float):
		"""Updates the GUI element."""
		pass
