import unittest

from unittest.mock import MagicMock

from src.mgmt.event_manager import EventManager
from src.mgmt.listener import Listener
from src.mgmt.event import Event

class DummyEvent(Event):
	def __init__(self, payload):
		super().__init__(event_type='foo')
		self.payload = payload

class EventManagerTest(unittest.TestCase):
	def test__pub_unsub(self):
		evt_mgr = EventManager()
		dummy = Listener()
		self.assertFalse(evt_mgr.is_subbed(evt_mgr))
		evt_mgr.sub('foo', dummy)
		evt_mgr.sub('bar', dummy)
		self.assertTrue(evt_mgr.is_subbed(dummy))
		self.assertTrue(evt_mgr.is_subbed_to_event('foo', dummy))
		self.assertTrue(evt_mgr.is_subbed_to_event('bar', dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('baz', dummy))
		evt_mgr.unsub('foo', dummy)
		self.assertTrue(evt_mgr.is_subbed(dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('foo', dummy))
		self.assertTrue(evt_mgr.is_subbed_to_event('bar', dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('baz', dummy))
		evt_mgr.unsub('bar', dummy)
		self.assertFalse(evt_mgr.is_subbed(dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('foo', dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('bar', dummy))
		self.assertFalse(evt_mgr.is_subbed_to_event('baz', dummy))

	def test__tick__publishes_events_on_next_tick(self):
		evt_mgr = EventManager()
		dummy = MagicMock(spec=Listener)
		evt_mgr.sub('foo', dummy)
		evt_mgr.tick(0.1, 1.0)
		self.assertEqual(dummy.update.call_count, 0)
		evt_mgr.pub(DummyEvent('bar'))
		self.assertEqual(dummy.update.call_count, 0)	
		evt_mgr.tick(0.1, 1.1)
		self.assertEqual(dummy.update.call_count, 1)

	def test__tick__doesnt_republish(self):
		evt_mgr = EventManager()
		dummy = MagicMock(spec=Listener)
		evt_mgr.sub('foo', dummy)
		evt_mgr.pub(DummyEvent('bar'))
		evt_mgr.tick(0.1, 1.0)
		self.assertEqual(dummy.update.call_count, 1)
		evt_mgr.tick(0.1, 1.1)
		self.assertEqual(dummy.update.call_count, 1)

if __name__ == "__main__":
	unittest.main()
