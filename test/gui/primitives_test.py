import unittest
from unittest.mock import Mock
import pygame
from src.gui.primitives import Button, Label, Panel, TextBox, Image
from src.gui.gui import GuiElement

class TestButton(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.surface = pygame.display.set_mode((800, 600))
		self.gui_mgr = Mock()
		self.gui_mgr.surface = self.surface

	def test_button_label(self):
		button = Button(rect=((0, 0), (100, 50)), text="Click Me", parent=None)
		button.gui_mgr = self.gui_mgr
		self.assertEqual(button.text, "Click Me")

	def test_button_callback(self):
		callback = Mock()
		button = Button(rect=((0, 0), (100, 50)), text="Click Me", callback=callback, parent=None)
		button.gui_mgr = self.gui_mgr
		event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(10, 10))
		button.process_event(event)
		callback.assert_called_once()

class TestLabel(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.surface = pygame.display.set_mode((800, 600))
		self.gui_mgr = Mock()
		self.gui_mgr.surface = self.surface

	def test_label_text(self):
		label = Label(rect=((0, 0), (100, 50)), text="Hello", parent=None)
		label.gui_mgr = self.gui_mgr
		self.assertEqual(label.text, "Hello")

class TestTextBox(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.surface = pygame.display.set_mode((800, 600))
		self.gui_mgr = Mock()
		self.gui_mgr.surface = self.surface

	def test_textbox_text(self):
		textbox = TextBox(rect=((0, 0), (100, 50)), text="Sample Text", parent=None)
		textbox.gui_mgr = self.gui_mgr
		self.assertEqual(textbox.text, "Sample Text")

class TestImage(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.surface = pygame.display.set_mode((800, 600))
		self.gui_mgr = Mock()
		self.gui_mgr.surface = self.surface

	def test_image_load(self):
		with self.assertRaises(ValueError):
			Image(rect=((0, 0), (100, 50)), image=None, parent=None)

if __name__ == '__main__':
	unittest.main()