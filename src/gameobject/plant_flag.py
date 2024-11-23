from src.mgmt.listener import Listener
from src.mgmt.event import Event

from src.gameobject.action import Action
from src.gameobject.interactable import Interactable

IMAGE_ID__FLAG__CLICK_HERE = "assets/img/sprite/click-here.png"
IMAGE_ID__FLAG__PLANTED = "assets/img/sprite/flag.png"

class PlantFlag(Interactable, Listener):
	"""
	Plant a flag to mark a location.
	"""

	_is_planted = False
	_is_first = False

	def __init__(self, game_mgr=None, pos=None, is_first=False):
		super().__init__(
			game_mgr=game_mgr,
			pos=pos,
			size=(1,1,0)
		)
		self._is_first = is_first
		self.evt_mgr.sub("flag.planted", self)

	def update(self, event):
		if event.event_type == "flag.planted":
			self._plant()

	def image_path(self):
		if not self._is_planted:
			return IMAGE_ID__FLAG__CLICK_HERE
		else:
			return IMAGE_ID__FLAG__PLANTED

	def _plant(self):
		self._is_planted = True
		self.size = (2,1,5)

	def _make_plant_flag_action(self):
		return Action(
			target=self,
			offset=(0,-1),
			display_label="Plant Flag",
			expected_value=None,
			event=FlagPlantedEvent()
		)

	def actions(self, player_id: int):
		if not self._is_planted and player_id == self.owner:
			return [
				self._make_plant_flag_action()
			]
		else:
			return []

class FlagPlantedEvent(Event):
	"""
	An event to fire when the flag has been planted.
	"""

	def __init__(self):
		super().__init__(event_type="flag.planted")
