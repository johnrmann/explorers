import unittest

from unittest.mock import MagicMock

from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager

from src.gameobject.lander import Lander
from src.gameobject.actor import Actor
from src.gameobject.actor_motives import ActorMotive
from src.gameobject.rabbit_hole import EnterRabbitHoleEvent, ExitRabbitHoleEvent

class LanderTest(unittest.TestCase):

	def setUp(self):
		evt_mgr = MagicMock(spec=EventManager)
		self.game_mgr = MagicMock(spec=GameManager)
		self.game_mgr.evt_mgr = evt_mgr
		self.game_mgr.utc = 0
		self.lander = Lander(game_mgr=self.game_mgr)
		self.actor = MagicMock(spec=Actor)

	def test__enter__actor_enters_lander(self):
		self.lander.game_mgr.utc = 100
		result = self.lander.enter(self.actor)
		self.assertTrue(result)
		self.assertIn(self.actor, self.lander.inside)
		self.assertEqual(self.lander.next_use_for_actor[self.actor], 120)
		self.assertEqual(self.lander.next_use, 110)

	def test__enter__actor_cannot_enter_full_lander(self):
		self.lander.enter(self.actor)
		actor2 = MagicMock(spec=Actor)
		result = self.lander.enter(actor2)
		self.assertFalse(result)

	def test__enter__via_evt_mgr(self):
		self.assertNotIn(self.actor, self.lander.inside)
		self.lander.game_mgr.utc = 100
		self.lander.update(
			EnterRabbitHoleEvent(
				actor=self.actor,
				rabbit_hole=self.lander,
			)
		)
		self.assertIn(self.actor, self.lander.inside)

	def test__tick__actor_fills_motive(self):
		# Mock actor's motives to return 50 when added.
		self.actor.motives.max = MagicMock(return_value=100)
		self.actor.motives.add = MagicMock(return_value=50)

		# Dispatch the event. We want to refill oxygen.
		self.lander.update(
			EnterRabbitHoleEvent(
				actor=self.actor,
				rabbit_hole=self.lander,
				data=ActorMotive.OXYGEN
			)
		)

		# The first tick should not remove the actor.
		self.lander.tick(1, 100)
		self.actor.motives.add.assert_called_once_with(ActorMotive.OXYGEN, 25)
		self.assertIn(self.actor, self.lander.inside)

		# The second tick should remove the actor.
		self.actor.motives.add = MagicMock(return_value=100)
		self.lander.tick(1, 101)
		self.assertNotIn(self.actor, self.lander.inside)

	def test__exit__actor_exits_lander(self):
		self.lander.inside.add(self.actor)
		self.lander.exit(self.actor)
		self.assertNotIn(self.actor, self.lander.inside)
		self.lander.evt_mgr.pub.assert_called_once_with(
			ExitRabbitHoleEvent(actor=self.actor, rabbit_hole=self.lander)
		)

	def test__actions__actor_can_perform_actions(self):
		self.lander.is_full = MagicMock(return_value=False)
		self.lander.game_mgr.utc = 100
		self.actor.owner = self.lander.owner
		actions = self.lander.actions(self.actor)
		self.assertEqual(len(actions), 3)
		self.assertEqual(actions[0].display_label, "Refill Oxygen")
		self.assertEqual(actions[1].display_label, "Have Meal")
		self.assertEqual(actions[2].display_label, "Sleep")

	def test__actions__actor_cannot_perform_actions_when_full(self):
		self.lander.is_full = MagicMock(return_value=True)
		actions = self.lander.actions(self.actor)
		self.assertEqual(len(actions), 0)

	def test__actions__actor_cannot_perform_actions_when_on_cooldown(self):
		self.lander.is_full = MagicMock(return_value=False)
		self.lander.game_mgr.utc = 100
		self.lander.next_use = 110
		actions = self.lander.actions(self.actor)
		self.assertEqual(len(actions), 0)

if __name__ == '__main__':
	unittest.main()
