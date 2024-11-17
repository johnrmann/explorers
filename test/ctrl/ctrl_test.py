import pygame
import unittest

from unittest.mock import MagicMock, Mock, patch

from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager

from src.ctrl.ctrl import Control
from src.ctrl.event_id import (
	EVENT_CAMERA_MOVE, EVENT_CAMERA_ROTATE, EVENT_CAMERA_ZOOM
)

class TestControl(unittest.TestCase):

	@patch('src.mgmt.singletons.get_game_manager')
	def setUp(self, mock_get_game_manager):
		self.mock_evt_mgr = MagicMock(spec=EventManager)
		self.mock_gui_mgr = Mock()
		self.mock_game_mgr = Mock(spec=GameManager)
		self.mock_game_mgr.evt_mgr = self.mock_evt_mgr
		self.mock_game_mgr.gui_mgr = self.mock_gui_mgr
		mock_get_game_manager.return_value = self.mock_game_mgr
		self.control = Control(self.mock_game_mgr)

	def test_interpret_pygame_camera_keyboard_event_move(self):
		event = Mock()
		event.key = pygame.K_UP
		with patch('src.ctrl.ctrl.pygame_key_to_camdir', return_value=(0, 1)):
			result = self.control.interpret_pygame_camera_keyboard_event(event)
			self.mock_evt_mgr.pub.assert_called_with(
				EVENT_CAMERA_MOVE,
				data=(0, 1)
			)
			self.assertTrue(result)

	def test_interpret_pygame_camera_keyboard_event_zoom(self):
		event = Mock()
		event.key = pygame.K_PLUS
		with patch(
			'src.ctrl.ctrl.pygame_key_to_delta_zoom',
			return_value=1
		):
			result = self.control.interpret_pygame_camera_keyboard_event(event)
			self.mock_evt_mgr.pub.assert_called_with(EVENT_CAMERA_ZOOM, data=1)
			self.assertTrue(result)

	def test_interpret_pygame_camera_keyboard_event_rotate(self):
		event = Mock()
		event.key = pygame.K_RIGHTBRACKET
		with patch(
			'src.ctrl.ctrl.pygame_key_to_delta_camera_rotate',
			return_value=15
		):
			result = self.control.interpret_pygame_camera_keyboard_event(event)
			self.mock_evt_mgr.pub.assert_called_with(EVENT_CAMERA_ROTATE, data=15)
			self.assertTrue(result)

	def test_interpret_pygame_event_quit(self):
		event = Mock()
		event.type = pygame.QUIT
		self.control.on_quit = Mock()
		result = self.control.interpret_pygame_event(event)
		self.control.on_quit.assert_called_once()
		self.assertTrue(result)

	def test_interpret_pygame_event_gui(self):
		event = Mock()
		self.mock_gui_mgr.process_event.return_value = True
		result = self.control.interpret_pygame_event(event)
		self.mock_gui_mgr.process_event.assert_called_once_with(event)
		self.assertTrue(result)

	def test_interpret_pygame_input(self):
		event = Mock()
		with patch('pygame.event.get', return_value=[event]):
			with patch.object(
				self.control,
				'interpret_pygame_event',
				return_value=True
			) as mock_method:
				self.control.interpret_pygame_input()
				mock_method.assert_called_once_with(event)

if __name__ == '__main__':
	unittest.main()
