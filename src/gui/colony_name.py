from src.gui.anchor import Anchor
from src.gui.gui import GuiElement
from src.gui.primitives import Panel
from src.gui.edit_label import EditLabel

from src.colony.colony import Colony

class ColonyName(GuiElement):
	"""
	This is something at the top of the screen that shows the name of the
	current colony, along with the player that owns it, and an edit button.
	"""

	_colony: Colony = None

	def __init__(self, **kwargs):
		super().__init__(
			origin=(0, 0),
			dimensions=(250, 50),
			anchor=Anchor.TOP_CENTER,
			**kwargs
		)
		self._panel = Panel(
			origin=(0, 0),
			dimensions=(250, 50),
			parent=self,
		)
		self._edit_label = EditLabel(
			origin=(0, 0),
			dimensions=(250, 50),
			parent=self,
			on_edit=self._on_edit,
			text='Colony Name',
		)

	def _on_edit(self):
		new_name = input('Enter new colony name: ')
		self._colony.name = new_name

	@property
	def colony(self):
		return self._colony

	@colony.setter
	def colony(self, new_colony):
		self._colony = new_colony
		if new_colony is None:
			self.hidden = True
		else:
			self.hidden = False
			self._edit_label.text = new_colony.name

	def my_update(self, dt: float):
		game_mgr = self.gui_mgr.game_mgr
		if game_mgr is None:
			return
		if len(game_mgr.colonies) != 0:
			self.colony = game_mgr.colonies[0]
