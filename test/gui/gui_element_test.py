import unittest

from unittest.mock import MagicMock, Mock

from src.gui.gui import GuiElement, _GuiManager
from src.gui.anchor import Anchor

class Dummy(GuiElement):
	"""
	A dummy class to test the GuiElement class.
	"""
	pass

class GuiElementTest(unittest.TestCase):
	def setUp(self):
		self.gui_mgr = MagicMock(spec=_GuiManager)
		self.gui_mgr.game_mgr = Mock()
		self.gui_mgr.elements = []
		self.gui_mgr.game_mgr.evt_mgr = Mock()
		self.gui_mgr.surface = Mock()
		self.gui_mgr.surface.get_size = lambda: (800, 600)

	def test__init__no_parent_attaches_to_mgr(self):
		elem = Dummy(gui_mgr=self.gui_mgr)
		self.assertEqual(elem.elements, [])
		self.assertEqual(elem.gui_mgr, self.gui_mgr)

	def test__init__with_parent(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		child = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		self.assertEqual(child.parent, parent)
		self.assertIn(child, parent.elements)

	def test__init__via_rect(self):
		elem = Dummy(gui_mgr=self.gui_mgr, rect=((5,5), (20,20)))
		self.assertEqual(elem.relative_origin, (5,5))
		self.assertEqual(elem.dimensions, (20,20))

	def test__origin__errors_if_undefiend(self):
		with self.assertRaises(ValueError):
			elem = Dummy(gui_mgr=self.gui_mgr)
			_ = elem.origin

	def test__origin__root(self):
		elem = Dummy(gui_mgr=self.gui_mgr, origin=(4,8))
		self.assertEqual(elem.origin, (4,8))

	def test__origin__parent(self):
		parent = Dummy(gui_mgr=self.gui_mgr, origin=(10,10))
		child = Dummy(gui_mgr=self.gui_mgr, parent=parent, origin=(10, 10))
		self.assertEqual(child.origin, (20,20))

	def test__origin__with_anchor(self):
		elem = Dummy(
			gui_mgr=self.gui_mgr,
			anchor=Anchor.BOTTOM_RIGHT,
			origin=(0, 0),
			dimensions=(10, 10)
		)
		self.assertEqual(elem.origin, (790,590))

	def test__origin__with_anchor_and_parent(self):
		parent = Dummy(gui_mgr=self.gui_mgr, origin=(5,5), dimensions=(40,40))
		child = Dummy(
			gui_mgr=self.gui_mgr,
			parent=parent,
			anchor=Anchor.TOP_RIGHT,
			origin=(0, 0),
			dimensions=(10, 10)
		)
		self.assertEqual(child.origin, (35,5))

	def test__pygame_rect(self):
		elem = Dummy(gui_mgr=self.gui_mgr, origin=(5,5), dimensions=(20,20))
		self.assertEqual(elem.pygame_rect, ((5,5), (20,20)))

	def test__pygame_rect__errors_if_no_dimensions(self):
		with self.assertRaises(ValueError):
			elem = Dummy(gui_mgr=self.gui_mgr)
			_ = elem.pygame_rect

	def test__draw__draws_children(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		child = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child.draw = Mock()
		parent.draw(self.gui_mgr.surface)
		self.assertEqual(child.draw.call_count, 1)

	def test__draw__skips_hidden_children(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		child1 = Dummy(gui_mgr=self.gui_mgr, parent=parent, hidden=True)
		child1.draw = Mock()
		child2 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child2.draw = Mock()
		parent.draw(self.gui_mgr.surface)
		self.assertEqual(child1.draw.call_count, 0)
		self.assertEqual(child2.draw.call_count, 1)

	def test__draw__skips_all_children_if_hidden(self):
		parent = Dummy(gui_mgr=self.gui_mgr, hidden=True)
		child1 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child1.draw = Mock()
		child2 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child2.draw = Mock()
		parent.draw(self.gui_mgr.surface)
		self.assertEqual(child1.draw.call_count, 0)
		self.assertEqual(child2.draw.call_count, 0)

	def test__process_event__if_no_children1(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		self.assertFalse(parent.process_event(Mock()))

	def test__process_event__if_no_children2(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		parent.do_process_event = lambda _: True
		self.assertTrue(parent.process_event(Mock()))

	def test__process_event__calls_children(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		child = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child.process_event = Mock()
		parent.process_event(Mock())
		self.assertEqual(child.process_event.call_count, 1)

	def test__process_event__skips_hidden_children(self):
		parent = Dummy(gui_mgr=self.gui_mgr)
		child1 = Dummy(gui_mgr=self.gui_mgr, parent=parent, hidden=True)
		child1.process_event = Mock()
		child2 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child2.process_event = Mock()
		parent.process_event(Mock())
		self.assertEqual(child1.process_event.call_count, 0)
		self.assertEqual(child2.process_event.call_count, 1)

	def test__process_event__skips_all_children_if_hidden(self):
		parent = Dummy(gui_mgr=self.gui_mgr, hidden=True)
		child1 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child1.process_event = Mock()
		child2 = Dummy(gui_mgr=self.gui_mgr, parent=parent)
		child2.process_event = Mock()
		parent.process_event(Mock())
		self.assertEqual(child1.process_event.call_count, 0)
		self.assertEqual(child2.process_event.call_count, 0)

if __name__ == '__main__':
	unittest.main()
