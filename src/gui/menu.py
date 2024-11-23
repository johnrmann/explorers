"""
Menus are lists of buttons.
"""

from src.gui.gui import GuiElement
from src.gui.layout import VerticalLayout, HorizontalLayout
from src.gui.primitives import Button

class MenuOption:
	"""Glorified tuple for menus options."""

	label: str
	callback: callable
	events: list[tuple[str, any]]

	def __init__(self, label=None, callback=None, event=None, events=None):
		if label is None:
			raise ValueError("Label required.")
		self.label = label
		self.callback = callback
		if event is not None:
			self.events = [event]
		else:
			self.events = events

class VerticalMenu(GuiElement):
	"""
	Shows a menu of buttons.
	"""

	def __init__(
			self,
			origin=None,
			width: int = 200,
			options: list[MenuOption] = None,
			parent: GuiElement = None,
	):
		super().__init__(parent=parent)
		self.relative_origin = origin
		self.layout = VerticalLayout(origin=(0,0), parent=self)
		for option in options:
			Button(
				rect=((0,0), (width,50)),
				text=option.label,
				callback=option.callback,
				events=option.events,
				parent=self,
			)

class HorizontalMenu(GuiElement):
	"""
	Shows a menu of buttons.
	"""

	def __init__(
			self,
			origin=None,
			height=50,
			options: list[MenuOption] = None,
			parent=None,
	):
		super().__init__(parent=parent)
		self.relative_origin = origin
		self.layout = HorizontalLayout(origin=(0,0), parent=self)
		for option in options:
			Button(
				rect=((0,0), (100,height)),
				text=option.label,
				callback=option.callback,
				events=option.events,
				parent=self,
			)
