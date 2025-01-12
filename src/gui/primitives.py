import pygame

from src.gui.gui import GuiElement
from src.gui.multiline import wrap_text

BUTTON_CHROME = 3

class Spacer(GuiElement):
	"""Empty space. Useful for auto layouts."""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)



class _BaseButton(GuiElement):
	"""Buttons can be clicked to trigger callbacks."""

	callback = None
	events = None

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


	def process_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.pygame_rect.collidepoint(event.pos):
				if callable(self.callback):
					self.callback()
				for event in self.events:
					self.evt_mgr.pub(event)
				return True
		return False



class Button(_BaseButton):
	"""This is a button with text."""

	text: str = None

	def __init__(self, text: str = "", **kwargs):
		super().__init__(**kwargs)
		self.text = text


	def my_draw(self, screen):
		pygame.draw.rect(screen, (0, 255, 255), self.pygame_rect)
		pygame.draw.rect(screen, (0, 0, 255), self._inner_pygame_rect)
		font = pygame.font.Font(None, 24)
		text_surface = font.render(self.text, True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=self._inner_pygame_rect.center)
		screen.blit(text_surface, text_rect)



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



class ImageButton(_BaseButton):
	"""A button with an image."""

	image_surface = None

	def __init__(
			self,
			image_surface=None,
			image_path=None,
			**kwargs
	):
		if image_surface is None and image_path is None:
			raise ValueError("Need an image object xor image path.")
		if image_surface is not None and image_path is not None:
			raise ValueError("Need an image object xor image path, not both.")
		super().__init__(**kwargs)
		if image_surface is not None:
			self.image_surface = image_surface
		else:
			self.image_surface = pygame.image.load(image_path).convert_alpha()


	def my_draw(self, screen):
		pygame.draw.rect(screen, (0, 255, 255), self.pygame_rect)
		pygame.draw.rect(screen, (0, 0, 255), self._inner_pygame_rect)
		transformed_image = pygame.transform.scale(
			self.image_surface,
			self._inner_pygame_rect.size
		)
		screen.blit(transformed_image, self._inner_pygame_rect)
