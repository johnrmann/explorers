from src.gui.gui import GuiElement
from src.gui.layout import VerticalLayout
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
