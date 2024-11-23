import pygame

from src.gameobject.actor import ActorDoActionEvent

from src.gui.gui import GuiElement
from src.gui.menu import VerticalMenu, MenuOption

def action_to_menu_option(action, actor):
	return MenuOption(
		label=action.display_label,
		events=[
			ActorDoActionEvent(actor, action),
		]
	)

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
		options = [
			action_to_menu_option(action, self.gui_mgr.game_mgr.player_character)
			for action in clicked.actions(1)
		]
		self.menu = VerticalMenu(
			origin=(0,0),
			width=width,
			options=options,
			parent=self,
		)

	def process_event(self, event):
		button_clicked = self.menu.process_event(event)
		if button_clicked:
			self.remove_me()
			return True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.remove_me()
			return True
		else:
			return False
