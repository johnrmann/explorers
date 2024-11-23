from src.mgmt.listener import Listener
from src.mgmt.event import Event

from src.gameobject.action import Action, EVENT_ID__DO_ACTION
from src.gameobject.interactable import Interactable

ACTION_ID__PLANT_FLAG = "action.plant_flag.plant_flag"

ACTION__PLANT_FLAG = Action(
	ACTION_ID__PLANT_FLAG,
	"Plant Flag",
	None
)

class PlantFlag(Interactable, Listener):
	"""
	Plant a flag to mark a location.
	"""

	_is_planted = False
	_is_first = False

	def __init__(self, pos=None, is_first=False):
		if pos is None:
			pos = (0,0)
		super().__init__(
			pos=pos,
			size=(1,1,0)
		)
		self._is_first = is_first

	def update(self, event_type, data):
		if event_type == EVENT_ID__DO_ACTION:
			if data == ACTION_ID__PLANT_FLAG:
				self._plant()

	def image_path(self):
		if not self._is_planted:
			return "assets/img/sprite/click-here.png"
		else:
			return "assets/img/sprite/flag.png"

	def _plant(self):
		self._is_planted = True
		self.size = (2,1,5)

	def _signal_plant(self):
		if self._is_first:
			self.evt_mgr.pub(FlagPlantedEvent())

	def actions(self, player_id: int):
		if not self._is_planted and player_id == self.owner:
			return [
				ACTION__PLANT_FLAG
			]
		else:
			return []

class FlagPlantedEvent(Event):
	def __init__(self):
		super().__init__(event_type="flag.planted")
