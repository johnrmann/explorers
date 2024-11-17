"""
Contains the class and action IDs for the lander.
"""

from src.gameobject.action import Action
from src.gameobject.interactable import Interactable
from src.gameobject.constants import FILL_OXYGEN

ACTION_ID__LANDER__REFILL_OXYGEN = "action.lander.refill_oxygen"

ACTION__LANDER__REFILL_OXYGEN = Action(
	ACTION_ID__LANDER__REFILL_OXYGEN,
	"Refill Oxygen",
	FILL_OXYGEN
)

class Lander(Interactable):
	"""
	At the start of the game, each player starts with a lander that can be
	used as a basic home base.
	"""

	def __init__(self, pos=None):
		if pos is None:
			pos = (0,0)
		super().__init__(
			pos=pos,
			size=(11,11)
		)

	def image_path(self):
		return "assets/img/lander.png"

	def actions(self, player_id: int):
		if player_id == self.owner:
			return [
				ACTION__LANDER__REFILL_OXYGEN
			]
		else:
			return []
