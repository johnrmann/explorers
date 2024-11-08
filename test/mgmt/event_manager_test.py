import unittest

from src.mgmt.event_manager import EventManager
from src.mgmt.listener import Listener

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

if __name__ == "__main__":
	unittest.main()
