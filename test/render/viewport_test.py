import unittest

from unittest.mock import MagicMock

from src.world.terrain import Terrain
from src.ctrl.event_id import (
	CameraMoveEvent,
	CameraZoomEvent,
	CameraRotateEvent
)
from src.render.viewport import Viewport, Direction

def make_terrain():
	map = [[1] * 32 for i in range(32)]
	return Terrain(map)

def make_viewport():
	vp = Viewport((800, 600), make_terrain())
	return vp

class ViewportTest(unittest.TestCase):
	def test__set_game_manager__subscribes_to_events(self):
		vp = make_viewport()
		game_mgr = MagicMock()
		game_mgr.evt_mgr = MagicMock()
		game_mgr.evt_mgr.sub = MagicMock()
		vp.game_mgr = game_mgr
		game_mgr.evt_mgr.sub.assert_called()


	def test__set_game_manager__write_once(self):
		vp = make_viewport()
		game_mgr = MagicMock()
		game_mgr.evt_mgr = MagicMock()
		vp.game_mgr = game_mgr
		with self.assertRaises(ValueError):
			vp.game_mgr = game_mgr


	def test__get_game_manager(self):
		vp = make_viewport()
		game_mgr = MagicMock()
		vp.game_mgr = game_mgr
		self.assertEqual(vp.game_mgr, game_mgr)


	def test__move_camera_noop(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_pos, (16, 16))
		vp.move_camera(None)
		self.assertEqual(vp.camera_pos, (16, 16))


	def test__move_camera__simple(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_pos, (16, 16))
		vp.move_camera(Direction.NORTHEAST)
		self.assertEqual(vp.camera_pos, (17, 15))
		vp.move_camera(Direction.SOUTHWEST)
		self.assertEqual(vp.camera_pos, (16, 16))
		vp.move_camera(Direction.NORTHWEST)
		self.assertEqual(vp.camera_pos, (15, 15))
		vp.move_camera(Direction.SOUTHEAST)
		self.assertEqual(vp.camera_pos, (16, 16))


	def test__move_camera__north_bounded(self):
		vp = make_viewport()
		vp.camera_pos = (16, 0)
		vp.move_camera(Direction.NORTH)
		self.assertEqual(vp.camera_pos, (16, 0))
		vp.move_camera(Direction.NORTHWEST)
		self.assertEqual(vp.camera_pos, (15, 0))


	def test__move_camera__south_bounded(self):
		vp = make_viewport()
		vp.camera_pos = (16, 31)
		vp.move_camera(Direction.SOUTH)
		self.assertEqual(vp.camera_pos, (16, 31))
		vp.move_camera(Direction.SOUTHEAST)
		self.assertEqual(vp.camera_pos, (17, 31))


	def test__move_camera__east_loops(self):
		vp = make_viewport()
		vp.camera_pos = (31, 0)
		vp.move_camera(Direction.EAST)
		self.assertEqual(vp.camera_pos, (0, 0))


	def test__move_camera__west_loops(self):
		vp = make_viewport()
		vp.camera_pos = (0, 0)
		vp.move_camera(Direction.WEST)
		self.assertEqual(vp.camera_pos, (31, 0))


	def test__move_camera__via_evt_mgr(self):
		vp = make_viewport()
		vp.camera_pos = (0, 0)
		vp.update(CameraMoveEvent(Direction.EAST))
		self.assertEqual(vp.camera_pos, (1,0))


	def test__zoom_camera__in(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 32)
		self.assertEqual(vp.tile_height, 16)
		vp.change_zoom(1)
		self.assertEqual(vp.tile_width, 64)
		self.assertEqual(vp.tile_height, 32)


	def test__zoom_camera__out(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 32)
		self.assertEqual(vp.tile_height, 16)
		vp.change_zoom(-1)
		self.assertEqual(vp.tile_width, 16)
		self.assertEqual(vp.tile_height, 8)


	def test__zoom_camera__nothing(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 32)
		self.assertEqual(vp.tile_height, 16)
		self.assertAlmostEqual(vp.tile_z, 16)
		vp.change_zoom(0)
		self.assertEqual(vp.tile_width, 32)
		self.assertEqual(vp.tile_height, 16)
		self.assertAlmostEqual(vp.tile_z, 16)


	def test__zoom_camera__via_evt_mgr(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 32)
		vp.update(CameraZoomEvent(1))
		self.assertEqual(vp.tile_width, 64)


	def test__rotate_camera__left(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_orientation, Direction.NORTHWEST)
		vp.rotate_camera(1)
		self.assertEqual(vp.camera_orientation, Direction.NORTHEAST)


	def test__rotate_camera__right(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_orientation, Direction.NORTHWEST)
		vp.rotate_camera(-1)
		self.assertEqual(vp.camera_orientation, Direction.SOUTHWEST)


	def test__rotate_camera__nothing(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_orientation, Direction.NORTHWEST)
		vp.rotate_camera(0)
		self.assertEqual(vp.camera_orientation, Direction.NORTHWEST)


	def test__rotate_camera__via_evt_mgr(self):
		vp = make_viewport()
		self.assertEqual(vp.camera_orientation, Direction.NORTHWEST)
		vp.update(CameraRotateEvent(1))
		self.assertEqual(vp.camera_orientation, Direction.NORTHEAST)


	def test__global_screen_position_to_screen_position(self):
		vp = make_viewport()
		vp.camera_pos = (15, 15)
		self.assertEqual(
			vp.global_screen_position_to_screen_position((0, 0)), (400, 60)
		)



if __name__ == "__main__":
	unittest.main()
