import pygame
import unittest

from unittest.mock import MagicMock, Mock, patch

from src.gui.playbar import PlaybarMode
from src.mgmt.event_manager import EventManager
from src.mgmt.game_manager import GameManager

from src.ctrl.ctrl import Control
from src.ctrl.event_id import (
	CameraZoomEvent, CameraMoveEvent
)
from src.ctrl.clickmap import ClickMap

def _make_click_event():
	event = Mock()
	event.type = pygame.MOUSEBUTTONDOWN
	return event


class TestControl(unittest.TestCase):

	@patch('src.mgmt.singletons.get_game_manager')
	def setUp(self, mock_get_game_manager):
		self.mock_evt_mgr = MagicMock(spec=EventManager)
		self.mock_evt_mgr.pub = Mock()
		self.mock_gui_mgr = Mock()
		self.mock_game_mgr = Mock(spec=GameManager)
		self.mock_game_mgr.evt_mgr = self.mock_evt_mgr
		self.mock_game_mgr.gui_mgr = self.mock_gui_mgr
		self.mock_game_mgr.remove_game_object = Mock()
		self.mock_game_mgr.add_game_object = Mock()
		mock_get_game_manager.return_value = self.mock_game_mgr

		self.screen_to_tile = Mock()
		self.screen_to_tile.return_value = (4, 8)

		self.clickmap = MagicMock(spec=ClickMap)
		self.clickmap.is_terrain = Mock()
		self.clickmap.is_terrain.return_value = True
		self.clickmap.game_object_at = Mock()
		self.clickmap.game_object_at.return_value = None

		self.mock_get_mouse_pos = Mock()
		self.mock_get_mouse_pos.return_value = (16, 16)

		self.control = Control(
			self.mock_game_mgr,
			screen_to_tile=self.screen_to_tile,
			get_mouse_pos=self.mock_get_mouse_pos,
			clickmap=self.clickmap,
		)


	def test__tick__updates_mouse_cell(self):
		"""
		Test that the control object updates the mouse position once per tick.
		"""
		self.control.tick(0.1)
		cell_x, cell_y = self.control.cell_under_mouse
		self.assertEqual(cell_x, 4)
		self.assertEqual(cell_y, 8)
		self.screen_to_tile.return_value = (15, 16)
		self.control.tick(0.1)
		cell_x, cell_y = self.control.cell_under_mouse
		self.assertEqual(cell_x, 15)
		self.assertEqual(cell_y, 16)


	def test__playbar_mode_changed__to_character__places_existing_object(self):
		new_object = MagicMock()

		self.control.playbar_mode_changed(PlaybarMode.BUILD)
		self.control.moving_game_object = new_object

		self.control.playbar_mode_changed(PlaybarMode.CHARACTER)
		self.assertIsNone(self.control.moving_game_object)
		self.control.game_mgr.remove_game_object.assert_not_called()


	def test__playbar_mode_changed__to_character__cancels_new_object(self):
		new_prototype = MagicMock()
		new_object = MagicMock()
		new_prototype.make = Mock()
		new_prototype.make.return_value = new_object

		self.control.playbar_mode_changed(PlaybarMode.BUILD)
		self.control.playbar_selected_build_object(new_prototype)
		self.control.game_mgr.add_game_object.assert_called_once_with(new_object)

		self.control.playbar_mode_changed(PlaybarMode.CHARACTER)
		self.assertIsNone(self.control.moving_game_object)
		self.control.game_mgr.remove_game_object.assert_called_once_with(new_object)


	def test__playbar_mode_changed__to_build__doesnt_move_character(self):
		"""
		Test that going to build mode disables character movement.
		"""
		self.control.tick(0.1)
		self.control.playbar_mode_changed(PlaybarMode.BUILD)

		self.clickmap.is_terrain.return_value = True
		self.clickmap.game_object_at.return_value = None
		self.control.interpret_pygame_event(_make_click_event())
		self.mock_evt_mgr.pub.assert_not_called()


	def test__playbar_mode_changed__to_build__moves_game_objects(self):
		"""
		Test that going to build mode allows us to select game objects.
		"""
		self.control.tick(0.1)
		self.control.playbar_mode_changed(PlaybarMode.BUILD)

		mock_gobj = Mock()
		self.clickmap.is_terrain.return_value = False
		self.clickmap.game_object_at.return_value = mock_gobj
		result = self.control.interpret_pygame_event(_make_click_event())
		self.assertTrue(result)


	def test__interpret_pygame_camera_keyboard_event__move(self):
		event = Mock()
		event.key = pygame.K_UP
		with patch('src.ctrl.ctrl.pygame_key_to_camdir', return_value=(0, 1)):
			result = self.control.interpret_pygame_camera_keyboard_event(event)
			self.mock_evt_mgr.pub.assert_called_with(
				CameraMoveEvent((0, 1))
			)
			self.assertTrue(result)


	def test__interpret_pygame_camera_keyboard_event__zoom(self):
		event = Mock()
		event.key = pygame.K_PLUS
		with patch(
			'src.ctrl.ctrl.pygame_key_to_delta_zoom',
			return_value=1
		):
			result = self.control.interpret_pygame_camera_keyboard_event(event)
			self.mock_evt_mgr.pub.assert_called_with(CameraZoomEvent(1))
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


	def test__playbar_selected_build_object__no_move(self):
		self.control.playbar_selected_build_object(MagicMock())
		self.assertIsNone(self.control.moving_game_object)


	def test__playbar_selected_build_object__makes_object(self):
		mock_prototype = MagicMock()
		mock_prototype.make = Mock()
		mock_prototype.make.return_value = new_obj = MagicMock()

		self.control.playbar_mode_changed(PlaybarMode.BUILD)
		self.control.playbar_selected_build_object(mock_prototype)

		self.assertEqual(self.control.moving_game_object, new_obj)


	def test__playbar_deselected_build_object__no_move(self):
		self.control.playbar_deselected_build_object()
		self.assertIsNone(self.control.moving_game_object)


	def test__playbar_deselected_build_object__removes_object(self):
		mock_prototype = MagicMock()
		mock_prototype.make = Mock()
		mock_prototype.make.return_value = MagicMock()

		self.control.playbar_mode_changed(PlaybarMode.BUILD)
		self.control.playbar_selected_build_object(mock_prototype)

		self.control.playbar_deselected_build_object()
		self.assertEqual(self.control.moving_game_object, None)
		self.mock_game_mgr.remove_game_object.assert_called_once()



if __name__ == '__main__':
	unittest.main()
