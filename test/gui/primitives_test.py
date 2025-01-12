import unittest
import pygame

from unittest.mock import Mock, patch

from src.mgmt.event_manager import EventManager

from src.gui.primitives import (
	Button,
	Label,
	Panel,
	TextBox,
	Image,
	ImageButton
)
from src.gui.gui import GuiElement

from test.gui.setup import make_mock_gui_manager

class PrimitivesTest(unittest.TestCase):
	def setUp(self):
		self.gui_mgr = make_mock_gui_manager()
		self.evt_mgr = self.gui_mgr.game_mgr.evt_mgr


	def test__button__label(self):
		button = Button(
			rect=((0, 0), (100, 50)),
			text="Click Me",
			parent=None,
			gui_mgr=self.gui_mgr
		)
		self.assertEqual(button.text, "Click Me")


	def test__button__callback(self):
		callback = Mock()
		button = Button(
			rect=((0, 0), (100, 50)),
			text="Click Me",
			callback=callback,
			parent=None,
			gui_mgr=self.gui_mgr
		)
		button.gui_mgr = self.gui_mgr
		event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(10, 10))
		button.process_event(event)
		callback.assert_called_once()


	def test__label__text(self):
		label = Label(
			rect=((0, 0), (100, 50)),
			text="Hello",
			parent=None,
			gui_mgr=self.gui_mgr
		)
		self.assertEqual(label.text, "Hello")


	def test__textbox__text(self):
		textbox = TextBox(
			rect=((0, 0), (100, 50)),
			text="Sample Text",
			parent=None,
			gui_mgr=self.gui_mgr
		)
		self.assertEqual(textbox.text, "Sample Text")


	def test__image__load(self):
		with self.assertRaises(ValueError):
			Image(
				rect=((0, 0), (100, 50)),
				image=None,
				parent=None,
				gui_mgr=self.gui_mgr
			)


	def test__image_button__invalid_neither(self):
		with self.assertRaises(ValueError):
			ImageButton()


	def test__image_button__invalid_both(self):
		with self.assertRaises(ValueError):
			ImageButton(
				image_path='assets/img/icon/pencil.png',
				image_surface='not allowed'
			)


	@patch('pygame.image.load')
	def test__image_button__loads_image(self, mock_load):
		return_mock = Mock()
		return_mock.convert_alpha.return_value = "Loaded!"
		mock_load.return_value = return_mock
		button = ImageButton(
			rect=((0, 0), (100, 50)),
			image_path='assets/img/icon/pencil.png',
			parent=None,
			gui_mgr=self.gui_mgr,
		)
		self.assertIsNotNone(button.image_surface)
		self.assertEqual(button.image_surface, "Loaded!")


if __name__ == '__main__':
	unittest.main()
