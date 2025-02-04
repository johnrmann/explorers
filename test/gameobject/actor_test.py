import unittest

from unittest.mock import MagicMock

from src.gameobject.rabbit_hole import EnterRabbitHoleEvent, ExitRabbitHoleEvent
from src.math.vector2 import Vector2
from src.mgmt.game_manager import GameManager
from src.mgmt.event_manager import EventManager
from src.mgmt.event import Event

from src.gameobject.action import Action
from src.gameobject.actor import (
	Actor,
	ActorDiedEvent,
	ActorDoActionEvent,
	MoveActorEvent
)

from test.setups import make_basic_game_manager

class MockEvent(Event):
	pass

class MockTarget:
	def __init__(self, pos=None):
		if pos is None:
			pos = Vector2(2,2)
		self.pos = pos

CARDINAL_PATH = [
	Vector2(0,0),
	Vector2(0,1),
	Vector2(1,1),
]



class ActorTest(unittest.TestCase):
	def setUp(self):
		game_mgr = make_basic_game_manager()
		self.actor = Actor(speed=1, game_mgr=game_mgr, pos=(0,0))
		self.actor.evt_mgr = MagicMock(spec=EventManager)
		self.actor.motives.hunger = 100
		self.actor.motives.oxygen = 100


	def tearDown(self):
		self.actor.evt_mgr.reset_mock()


	def test__moves_on_path(self):
		actor = self.actor
		actor._path_runner.path = (CARDINAL_PATH)
		check_idx = 0
		while actor.is_moving:
			self.assertEqual(actor.pos, CARDINAL_PATH[check_idx])
			actor.tick(1, check_idx)
			check_idx += 1


	def test__moves__via_event(self):
		actor = self.actor
		actor.update(MoveActorEvent(actor=actor, to_position=Vector2(1,1)))
		utc = 0
		while actor.is_moving:
			actor.tick(1, utc)
			utc += 1
		self.assertEqual(actor.pos, Vector2(1,1))


	def test__hides__when_enter_rabbit_hole(self):
		actor = self.actor
		actor.update(EnterRabbitHoleEvent(actor=actor))
		self.assertTrue(actor.hidden)


	def test__unhides__when_exit_rabbit_hole(self):
		actor = self.actor
		actor.update(EnterRabbitHoleEvent(actor=actor))
		actor.update(ExitRabbitHoleEvent(actor=actor))
		self.assertFalse(actor.hidden)


	def test__moves__to_action_position(self):
		target = MockTarget()
		action = Action(
			event=MockEvent(),
			display_label="Test Action",
			offset=Vector2(-1,0),
			expected_value=None,
			target=target
		)
		actor = self.actor
		actor.update(ActorDoActionEvent(actor=actor, action=action))
		utc = 0
		while actor.is_moving:
			actor.tick(1, utc)
			utc += 1
		targ_x, targ_y = target.pos
		offset_x, offset_y = action.offset
		self.assertEqual(
			actor.pos,
			Vector2(targ_x + offset_x, targ_y + offset_y)
		)


	def test__moves__fires_event_after_moving_to_action(self):
		target = MockTarget()
		event = MockEvent()
		action = Action(
			event=event,
			display_label="Test Action",
			offset=Vector2(-1,0),
			expected_value=None,
			target=target
		)
		actor = self.actor
		actor.update(ActorDoActionEvent(actor=actor, action=action))
		utc = 0
		while actor.is_moving:
			actor.tick(1, utc)
			utc += 1
		actor.evt_mgr.pub.assert_called_with(event)


	def test__dies_when_hunger_depletes(self):
		actor = self.actor
		actor.motives.hunger = 10
		while actor.motives.hunger > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())


	def test__dies_when_oxygen_depletes(self):
		actor = self.actor
		actor.motives.oxygen = 10
		while actor.motives.oxygen > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())


	def test__evt_mgr_gets_died_from_hunger(self):
		actor = self.actor
		actor.motives.hunger = 10
		while actor.motives.hunger > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())
		actor.evt_mgr.pub.assert_called_with(ActorDiedEvent(actor))


	def test__evt_mgr_gets_died_from_oxygen(self):
		actor = self.actor
		actor.motives.oxygen = 10
		while actor.motives.oxygen > 0:
			actor.tick(25, 0)
		self.assertTrue(actor.is_dead())
		actor.evt_mgr.pub.assert_called_with(ActorDiedEvent(actor))


	def test__motives_decrease_over_time(self):
		actor = self.actor
		initial_hunger = actor.motives.hunger
		initial_oxygen = actor.motives.oxygen
		actor.tick(1, 0)
		self.assertLess(actor.motives.hunger, initial_hunger)
		self.assertLess(actor.motives.oxygen, initial_oxygen)


	def test__motives_decrease_faster_when_moving(self):
		actor = self.actor
		actor._path_runner.path = CARDINAL_PATH
		o2_init, hunger_init, _, _ = actor.motives
		actor.tick(1, 0)
		o2_mvmt, hunger_mvmt, _, _ = actor.motives

		actor.motives.hunger = o2_init
		actor.motives.oxygen = hunger_init
		actor._path_runner.path = None

		actor.tick(1, 0)
		o2_still, hunger_still, _, _ = actor.motives

		self.assertLess(hunger_mvmt, hunger_still)
		self.assertLess(o2_mvmt, o2_still)



class ActorEventTest(unittest.TestCase):
	def test__move_event__equality_true(self):
		actor = MagicMock()
		event1 = MoveActorEvent(actor=actor, to_position=Vector2(1,1))
		event2 = MoveActorEvent(actor=actor, to_position=Vector2(1,1))
		self.assertEqual(event1, event2)


	def test__move_event__equality_false(self):
		actor1 = MagicMock()
		actor2 = MagicMock()
		event1 = MoveActorEvent(actor=actor1, to_position=Vector2(1,1))
		event2 = MoveActorEvent(actor=actor2, to_position=Vector2(1,1))
		self.assertNotEqual(event1, event2)
		event3 = MoveActorEvent(actor=actor1, to_position=Vector2(1,2))
		self.assertNotEqual(event1, event3)
		event4 = ActorDiedEvent(actor=actor1)
		self.assertNotEqual(event1, event4)


	def test__do_action_event__equality_true(self):
		actor = MagicMock()
		action = MagicMock()
		event1 = ActorDoActionEvent(actor=actor, action=action)
		event2 = ActorDoActionEvent(actor=actor, action=action)
		self.assertEqual(event1, event2)


	def test__do_action_event__equality_false(self):
		actor1 = MagicMock()
		actor2 = MagicMock()
		action1 = MagicMock()
		action2 = MagicMock()
		event1 = ActorDoActionEvent(actor=actor1, action=action1)
		event2 = ActorDoActionEvent(actor=actor2, action=action1)
		self.assertNotEqual(event1, event2)
		event3 = ActorDoActionEvent(actor=actor1, action=action2)
		self.assertNotEqual(event1, event3)
		event4 = ActorDiedEvent(actor=actor1)
		self.assertNotEqual(event1, event4)


	def test__died_event__equality_true(self):
		actor = MockTarget()
		event1 = ActorDiedEvent(actor=actor)
		event2 = ActorDiedEvent(actor=actor)
		self.assertEqual(event1, event2)


	def test__died_event__equality_false(self):
		event1 = ActorDiedEvent(actor=MockTarget())
		event2 = ActorDiedEvent(actor=MockTarget())
		self.assertNotEqual(event1, event2)
		event3 = ActorDoActionEvent(actor=MockTarget(), action=Action())
		self.assertNotEqual(event1, event3)



if __name__ == "__main__":
	unittest.main()
