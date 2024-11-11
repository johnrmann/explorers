import unittest

import pygame
import pygame_gui

from src.gui.gui import init_gui_manager
from src.gui.primitives import Button, Label, Panel
from unittest.mock import Mock
from unittest.mock import patch

class TestGuiPrimitives(unittest.TestCase):
	def setUp(self):
		pygame.init()
		self.screen = pygame.display.set_mode((800, 600))
		init_gui_manager()
		self.manager = pygame_gui.UIManager((800, 600))

	def test__button(self):
		button = Button(
			rect=((50, 50), (100, 50)),
			label="Click Me",
			container=None
		)
		self.assertIsInstance(button, Button)

	def test__label(self):
		label = Label(
			rect=((50, 150), (200, 50)),
			text="Hello World",
			container=None
		)
		self.assertIsInstance(label, Label)
		self.assertEqual(label.label.text, "Hello World")

	def test__panel(self):
		panel = Panel(
			rect=((50, 250), (300, 200))
		)
		self.assertIsInstance(panel, Panel)
		self.assertIsInstance(panel.pygame_container, pygame_gui.elements.UIPanel)

	def tearDown(self):
		pygame.quit()

if __name__ == '__main__':
	unittest.main()
	