import unittest
import pygame

from unittest.mock import Mock, MagicMock

from src.mgmt.event_manager import EventManager

from src.gui.primitives import Button, Label, Panel, TextBox, Image
from src.gui.gui import GuiElement

class PrimitivesTest(unittest.TestCase):
	def setUp(self):
		self.evt_mgr = MagicMock(spec=EventManager)
		pygame.init()
		self.surface = pygame.display.set_mode((800, 600))
		self.gui_mgr = Mock()
		self.gui_mgr.surface = self.surface

	def test_button_label(self):
		button = Button(
			rect=((0, 0), (100, 50)),
			text="Click Me",
			parent=None,
			evt_mgr=self.evt_mgr
		)
		button.gui_mgr = self.gui_mgr
		self.assertEqual(button.text, "Click Me")

	def test_button_callback(self):
		callback = Mock()
		button = Button(rect=((0, 0), (100, 50)), text="Click Me", callback=callback, parent=None, evt_mgr=self.evt_mgr)
		button.gui_mgr = self.gui_mgr
		event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(10, 10))
		button.process_event(event)
		callback.assert_called_once()

	def test_label_text(self):
		label = Label(
			rect=((0, 0), (100, 50)),
			text="Hello",
			parent=None,
			evt_mgr=self.evt_mgr
		)
		label.gui_mgr = self.gui_mgr
		self.assertEqual(label.text, "Hello")

	def test_textbox_text(self):
		textbox = TextBox(rect=((0, 0), (100, 50)), text="Sample Text", parent=None, evt_mgr=self.evt_mgr)
		textbox.gui_mgr = self.gui_mgr
		self.assertEqual(textbox.text, "Sample Text")

	def test_image_load(self):
		with self.assertRaises(ValueError):
			Image(rect=((0, 0), (100, 50)), image=None, parent=None, evt_mgr=self.evt_mgr)

if __name__ == '__main__':
	unittest.main()