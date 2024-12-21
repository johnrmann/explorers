import pygame

from src.gui.gui import GuiElement
from src.gui.primitives import Panel, Label

class FpsCounter(GuiElement):
	"""
	Renders the frames per second on the screen.
	"""

	def __init__(self):
		super().__init__()
		self.panel = Panel(rect=((0,0), (100,30)), parent=self)
		self.label = Label(rect=((0,0), (100,30)), parent=self.panel, text="00")
		self.clock = pygame.time.Clock()

	def my_update(self, dt):
		fps = self.clock.get_fps()
		self.label.text = f"FPS: {int(fps)}"
		self.clock.tick()

	@property
	def origin(self):
		w, __ = self.dimensions
		screen_w, __ = self.gui_mgr.surface.get_size()
		return ((screen_w - w), 0)

	@property
	def dimensions(self):
		return (100, 30)
