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
	@patch('pygame.transform.scale')
	def test__image_button__loads_image(self, mock_load, mock_scale):
		return_mock = Mock()
		scale_mock = Mock()

		load_surface = pygame.Surface((100, 50))
		scale_surface = pygame.Surface((100, 50))

		return_mock.convert_alpha.return_value = load_surface
		scale_mock.return_value = scale_surface

		mock_load.return_value = return_mock
		mock_scale.return_value = scale_mock

		button = ImageButton(
			rect=((0, 0), (100, 50)),
			image_path='assets/img/icon/pencil.png',
			parent=None,
			gui_mgr=self.gui_mgr,
		)
		self.assertIsNotNone(button.image_surface)


if __name__ == '__main__':
	unittest.main()
