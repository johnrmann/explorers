import pygame

from src.gui.gui import GuiElement
from src.gui.multiline import wrap_text

BUTTON_CHROME = 3

class Spacer(GuiElement):
	"""Empty space. Useful for auto layouts."""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Button(GuiElement):
	"""Buttons can be clicked to trigger callbacks."""

	text = None

	def __init__(self, text="", callback=None, events=None, **kwargs):
		super().__init__(**kwargs)
		self.text = text
		self.callback = callback
		if events is None:
			events = []
		self.events = events

	@property
	def _inner_pygame_rect(self):
		x, y, w, h = self.pygame_rect
		return pygame.Rect(
			x + BUTTON_CHROME,
			y + BUTTON_CHROME,
			w - (BUTTON_CHROME * 2),
			h - (BUTTON_CHROME * 2)
		)

	def my_draw(self, screen):
		pygame.draw.rect(screen, (0, 255, 255), self.pygame_rect)
		pygame.draw.rect(screen, (0, 0, 255), self._inner_pygame_rect)
		font = pygame.font.Font(None, 24)
		text_surface = font.render(self.text, True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=self._inner_pygame_rect.center)
		screen.blit(text_surface, text_rect)

	def process_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.pygame_rect.collidepoint(event.pos):
				if callable(self.callback):
					self.callback()
				for event in self.events:
					self.evt_mgr.pub(event)
				return True
		return False

class Label(GuiElement):
	"""Labels show text on the sceren."""

	text = ""

	def __init__(self, text="", **kwargs):
		super().__init__(**kwargs)
		self.text = text

	def my_draw(self, screen):
		font = pygame.font.Font(None, 24)
		text_surface = font.render(self.text, True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=self.pygame_rect.center)
		screen.blit(text_surface, text_rect)

class Panel(GuiElement):
	"""Panels are basically rects. Will add some more dressing on them soon."""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def my_draw(self, screen):
		pygame.draw.rect(screen, (0, 0, 255), self.pygame_rect)

class TextBox(GuiElement):
	"""Multi-line labels."""

	text = ""

	def __init__(self, text="", **kwargs):
		super().__init__(**kwargs)
		self.text = text

	def my_draw(self, screen):
		# Starting from the top of the pygame_rect, draw lines of text from
		# _text such that they all fit in the bounding box.
		font = pygame.font.Font(None, 24)
		lines = wrap_text(self.text, font, self.pygame_rect.width - 10)
		y = self.pygame_rect.top + 5
		for line in lines:
			text_draw = font.render(line, True, (255, 255, 255))
			screen.blit(text_draw, (self.pygame_rect.left + 5, y))
			y += 26

class Image(GuiElement):
	"""An image drawn on the screen within a rect."""

	def __init__(self, image=None, **kwargs):
		super().__init__(**kwargs)
		if image is None:
			raise ValueError("Need either an image object or image path.")
		if isinstance(image, str):
			self.image_surface = pygame.image.load(image).convert_alpha()
		else:
			self.image_surface = image

	def my_draw(self, screen):
		transformed_image = pygame.transform.scale(
			self.image_surface,
			self.dimensions
		)
		screen.blit(transformed_image, self.pygame_rect)
