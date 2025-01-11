import unittest

from unittest.mock import MagicMock, Mock

from src.mgmt.event_manager import EventManager
from src.gameobject.flora import Flora, FloraPrototype, FloraDiedEvent
from src.world.atmosphere import AtmosphereChangeTransformEvent, AtmosphereElement

def make_prototype():
	return FloraPrototype(
		name='Test Tree',
		tpr_range=(275, 300),
		tpr_damage_rate=1,
		tpr_recovery_rate=2,
		carbon_sequestration=1,
		max_health=100
	)



class TestFloraPrototype(unittest.TestCase):
	def setUp(self):
		self.prototype = make_prototype()


	def test__init__unpacks_tpr_range(self):
		self.assertEqual(self.prototype.min_tpr, 275)
		self.assertEqual(self.prototype.max_tpr, 300)


	def test__init__requires_name(self):
		with self.assertRaises(ValueError):
			FloraPrototype()


	def test__init__defaults_tpr_range(self):
		prototype = FloraPrototype(name='Test Tree')
		self.assertEqual(prototype.min_tpr, 255)
		self.assertEqual(prototype.max_tpr, 322)


	def test__tpr_health_delta__recovery(self):
		delta = self.prototype.tpr_health_delta(287.5)
		self.assertEqual(delta, 2)


	def test__tpr_health_delta__damage_below(self):
		delta = self.prototype.tpr_health_delta(274)
		self.assertEqual(delta, -1)


	def test__tpr_health_delta__damage_above(self):
		delta = self.prototype.tpr_health_delta(301)
		self.assertEqual(delta, -1)


	def test__tpr_health_delta__damage_way_below(self):
		delta = self.prototype.tpr_health_delta(250)
		self.assertEqual(delta, -25)


	def test__tpr_health_delta__damage_way_above(self):
		delta = self.prototype.tpr_health_delta(310)
		self.assertEqual(delta, -10)



class TestFlora(unittest.TestCase):
	def setUp(self):
		self.game_mgr = MagicMock()
		self.evt_mgr = MagicMock(spec=EventManager)
		self.game_mgr.evt_mgr = self.evt_mgr
		self.flora = Flora(prototype=make_prototype(), game_mgr=self.game_mgr)
		self.flora.evt_mgr = MagicMock()


	def test__init__requires_prototype(self):
		with self.assertRaises(ValueError):
			_ = Flora()


	def test__init__defaults_health(self):
		self.assertEqual(self.flora.health, 100)


	def test__on_init__publishes_atmosphere_change_delta_event(self):
		self.flora.on_init()
		self.flora.evt_mgr.pub.assert_called_once_with(
			AtmosphereChangeTransformEvent({
				(AtmosphereElement.CARBON, AtmosphereElement.OXYGEN): (1, 1)
			})
		)


	def test__on_remove__publishes_atmosphere_change_delta_event(self):
		self.flora.on_remove()
		self.flora.evt_mgr.pub.assert_called_once_with(
			AtmosphereChangeTransformEvent({
				(AtmosphereElement.CARBON, AtmosphereElement.OXYGEN): (-1, -1)
			})
		)


	def test__tick__good_tprs(self):
		"""
		Test that health doesn't change if the temperature is within the
		acceptable range.
		"""
		self.flora.prototype.tpr_health_delta = Mock(return_value=0)
		self.flora.tick(1, 0)
		self.assertEqual(self.flora.health, 100)


	def test__tick__decreases_health_proportional_dt(self):
		"""
		Test that the health changes according to delta time.
		"""
		self.flora.prototype.tpr_health_delta = Mock(return_value=-1)
		self.flora.tick(1, 0)
		self.assertEqual(self.flora.health, 99)
		self.flora.tick(2, 0)
		self.assertEqual(self.flora.health, 97)


	def test__tick__health_capped_at_max(self):
		"""
		Test that health doesn't exceed the maximum health.
		"""
		self.flora.prototype.tpr_health_delta = Mock(return_value=10)
		self.flora.health = 99
		self.flora.tick(1, 0)
		self.assertEqual(self.flora.health, 100)


	def test__tick__health_capped_at_min(self):
		"""
		Test that health doesn't go below zero.
		"""
		self.flora.prototype.tpr_health_delta = Mock(return_value=-10)
		self.flora.health = 1
		self.flora.tick(1, 0)
		self.assertEqual(self.flora.health, 0)


	def test__tick__sends_died_event(self):
		"""
		Test that health going to zero sends a FloraDiedEvent.
		"""
		self.flora.prototype.tpr_health_delta = Mock(return_value=-1)
		self.flora.health = 1
		self.flora.tick(1, 0)
		self.flora.evt_mgr.pub.assert_called_once_with(
			FloraDiedEvent(flora=self.flora)
		)



class TestFloraDiedEvent(unittest.TestCase):
	def test__init__requires_flora(self):
		with self.assertRaises(ValueError):
			_ = FloraDiedEvent(None)


	def test__init__stores_flora(self):
		flora = MagicMock(spec=Flora)
		event = FloraDiedEvent(flora)
		self.assertEqual(event.flora, flora)


	def test__eq__matches_same(self):
		flora1 = MagicMock(spec=Flora)
		flora2 = MagicMock(spec=Flora)
		event1 = FloraDiedEvent(flora1)
		event2 = FloraDiedEvent(flora2)
		self.assertEqual(event1 == event2, False)



if __name__ == '__main__':
	unittest.main()
