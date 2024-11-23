import unittest

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
		self.assertEqual(vp.tile_width, 24)
		self.assertEqual(vp.tile_height, 12)
		self.assertAlmostEqual(vp.tile_z**2, 180)
		vp.change_zoom(1)
		self.assertEqual(vp.tile_width, 48)
		self.assertEqual(vp.tile_height, 24)
		self.assertAlmostEqual(vp.tile_z**2, 720)
	
	def test__zoom_camera__out(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 24)
		self.assertEqual(vp.tile_height, 12)
		self.assertAlmostEqual(vp.tile_z**2, 180)
		vp.change_zoom(-1)
		self.assertEqual(vp.tile_width, 12)
		self.assertEqual(vp.tile_height, 6)
		self.assertAlmostEqual(vp.tile_z**2, 45)

	def test__zoom_camera__nothing(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 24)
		self.assertEqual(vp.tile_height, 12)
		self.assertAlmostEqual(vp.tile_z**2, 180)
		vp.change_zoom(0)
		self.assertEqual(vp.tile_width, 24)
		self.assertEqual(vp.tile_height, 12)
		self.assertAlmostEqual(vp.tile_z**2, 180)
	
	def test__zoom_camera__via_evt_mgr(self):
		vp = make_viewport()
		self.assertEqual(vp.tile_width, 24)
		vp.update(CameraZoomEvent(1))
		self.assertEqual(vp.tile_width, 48)
	
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
	
if __name__ == "__main__":
	unittest.main()
