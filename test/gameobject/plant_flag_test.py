import unittest

from unittest.mock import MagicMock

from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager

from src.gameobject.actor import Actor
from src.gameobject.plant_flag import (
	PlantFlag,
	FlagPlantedEvent,
	IMAGE_ID__FLAG__CLICK_HERE,
	IMAGE_ID__FLAG__PLANTED,
)

class PlantFlagTest(unittest.TestCase):

	def setUp(self):
		evt_mgr = MagicMock(spec=EventManager)
		self.game_mgr = MagicMock(spec=GameManager)
		self.game_mgr.evt_mgr = evt_mgr
		self.actor = Actor(game_mgr=self.game_mgr, owner=1)
		self.plant_flag = PlantFlag(game_mgr=self.game_mgr, pos=(5, 5))

	def test__init__attributes(self):
		self.assertEqual(self.plant_flag.pos, (5, 5))
		self.assertEqual(self.plant_flag.size, (1, 1, None))
		self.assertEqual(self.plant_flag.game_mgr, self.game_mgr)

	def test__update__flag_planted_event(self):
		self.assertEqual(
			self.plant_flag.image_path(),
			IMAGE_ID__FLAG__CLICK_HERE
		)
		event = FlagPlantedEvent()
		self.plant_flag.update(event)
		self.assertEqual(
			self.plant_flag.image_path(),
			IMAGE_ID__FLAG__PLANTED
		)

	def test__actions__not_planted(self):
		self.plant_flag.owner = 1
		actions = self.plant_flag.actions(actor=self.actor)
		self.assertEqual(len(actions), 1)
		self.assertEqual(actions[0].display_label, "Plant Flag")

	def test__actions__not_owned(self):
		self.plant_flag.owner = 2
		actions = self.plant_flag.actions(actor=self.actor)
		self.assertEqual(len(actions), 0)

	def test__actions__planted(self):
		event = FlagPlantedEvent()
		self.plant_flag.update(event)
		actions = self.plant_flag.actions(actor=self.actor)
		self.assertEqual(len(actions), 0)

if __name__ == '__main__':
	unittest.main()
