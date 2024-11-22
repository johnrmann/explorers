import pygame

from src.gui.gui import GuiElement
from src.gui.menu import VerticalMenu

class ActionMenu(GuiElement):
	"""
	For interacting with game objects.
	"""

	def __init__(
			self,
			origin=None,
			width=200,
			parent=None,
			clicked=None,
	):
		super().__init__(parent=parent)
		self.relative_origin = origin
		action_txts = [action.display_label for action in clicked.actions(1)]
		self.menu = VerticalMenu(
			origin=(0,0),
			width=width,
			actions=action_txts,
			parent=self,
		)

	def process_event(self, event):
		button_clicked = self.menu.process_event(event)
		if button_clicked:
			print("CLICKED!!!")
			# TODO(mannjohn) - trigger the action.
			return True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.remove_me()
			return True
		else:
			return False
