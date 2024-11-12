import pygame
import pygame_gui

from typing import Callable

from src.gui.gui import GuiElement

class Button(GuiElement):
	_text_func: Callable[[float], str] = None

	def __init__(self, rect=None, label="", callback=None, container=None):
		super().__init__()
		if container is not None:
			container = container.pygame_container
		if callable(label):
			self._text_func = label
			label = label(0)
		self.button = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect(rect),
			text=label,
			manager=self.pygame_manager,
			container=container
		)
		self.gui_mgr.element_to_callback[self.button] = callback

	def __del__(self):
		self.gui_mgr.element_to_callback[self.button] = None
		self.button.kill()

	def update(self, dt: float):
		if self._text_func is not None:
			self.button.set_text(self._text_func(dt))

class Label(GuiElement):
	_text_func: Callable[[float], str] = None

	def __init__(self, rect=None, text="", container=None):
		super().__init__()
		if container is not None:
			container = container.pygame_container
		if callable(text):
			self._text_func = text
			text = text(0)
		self.label = pygame_gui.elements.UILabel(
			relative_rect=pygame.Rect(rect),
			text=text,
			manager=self.pygame_manager,
			container=container
		)

	def __del__(self):
		self.label.kill()

	def update(self, dt: float):
		if self._text_func is not None:
			self.label.set_text(self._text_func(dt))

class Panel(GuiElement):
	def __init__(self, rect=None):
		super().__init__()
		origin, dimension = rect
		x, y = origin
		width, height = dimension
		panel_rect = pygame.Rect(x, y, width, height)
		self.panel = pygame_gui.elements.UIPanel(
			relative_rect=panel_rect,
			manager=self.pygame_manager,
		)

	def __del__(self):
		self.panel.kill()

	@property
	def pygame_container(self):
		return self.panel

class TextBox(GuiElement):
	_text_func: Callable[[float], str] = None

	def __init__(self, rect=None, text="", container=None):
		super().__init__()
		if container is not None:
			container = container.pygame_container
		if callable(text):
			self._text_func = text
			text = text(0)
		textbox_rect = pygame.Rect(rect)
		self.textbox = pygame_gui.elements.UITextBox(
			html_text=text,
			relative_rect=textbox_rect,
			manager=self.pygame_manager,
			container=container
		)

	def __del__(self):
		self.textbox.kill()

	@property
	def pygame_container(self):
		return self.textbox

	def update(self, dt: float):
		if self._text_func is not None:
			self.textbox.set_html_text(self._text_func(dt))

class Image(GuiElement):
	def __init__(self, rect=None, image=None, container=None):
		super().__init__()
		origin, dimension = rect
		if image is None:
			raise ValueError("Need either an image object or image path.")
		if container is not None:
			container = container.pygame_container
		x, y = origin
		width, height = dimension
		image_rect = pygame.Rect(x, y, width, height)
		if isinstance(image, str):
			image_surface = pygame.image.load(image).convert_alpha()
		else:
			image_surface = image
		self.image = pygame_gui.elements.UIImage(
			relative_rect=image_rect,
			image_surface=image_surface,
			manager=self.pygame_manager,
			container=container
		)

	def __del__(self):
		self.image.kill()

	@property
	def pygame_container(self):
		return self.image