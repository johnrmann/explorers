"""
Menus are lists of buttons.
"""

from src.gui.gui import GuiElement
from src.gui.layout import VerticalLayout, HorizontalLayout
from src.gui.primitives import Button

class VerticalMenu(GuiElement):
	"""
	Shows a menu of buttons.
	"""

	def __init__(
			self,
			origin=None,
			width=200,
			actions=None,
			parent=None,
	):
		super().__init__(parent=parent)
		self.layout = VerticalLayout(origin=origin)
		for action_txt in actions:
			Button(
				rect=((0,0), (width,50)),
				text=action_txt,
				parent=self.layout
			)

class HorizontalMenu(GuiElement):
	"""
	Shows a menu of buttons.
	"""

	def __init__(
			self,
			origin=None,
			height=50,
			actions=None,
			parent=None,
	):
		super().__init__(parent=parent)
		self.layout = HorizontalLayout(origin=origin)
		for action_txt in actions:
			Button(
				rect=((0,0), (100,height)),
				text=action_txt,
				parent=self.layout
			)
