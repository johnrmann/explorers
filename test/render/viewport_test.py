import unittest

from src.world.terrain import Terrain
from src.render.viewport import Viewport, CameraDirection

def make_terrain():
    map = [[1] * 32 for i in range(32)]
    return Terrain(map)

def make_viewport():
    return Viewport((800, 600), make_terrain())

class ViewportTest(unittest.TestCase):
    def test__move_camera__simple(self):
        vp = make_viewport()
        self.assertEqual(vp.camera_pos, (16, 16))
        vp.move_camera(CameraDirection.NORTHEAST)
        self.assertEqual(vp.camera_pos, (17, 15))
        vp.move_camera(CameraDirection.SOUTHWEST)
        self.assertEqual(vp.camera_pos, (16, 16))
        vp.move_camera(CameraDirection.NORTHWEST)
        self.assertEqual(vp.camera_pos, (15, 15))
        vp.move_camera(CameraDirection.SOUTHEAST)
        self.assertEqual(vp.camera_pos, (16, 16))
    
    def test__move_camera__north_bounded(self):
        vp = make_viewport()
        vp.camera_pos = (16, 0)
        vp.move_camera(CameraDirection.NORTH)
        self.assertEqual(vp.camera_pos, (16, 0))
        vp.move_camera(CameraDirection.NORTHWEST)
        self.assertEqual(vp.camera_pos, (15, 0))
    
    def test__move_camera__south_bounded(self):
        vp = make_viewport()
        vp.camera_pos = (16, 31)
        vp.move_camera(CameraDirection.SOUTH)
        self.assertEqual(vp.camera_pos, (16, 31))
        vp.move_camera(CameraDirection.SOUTHEAST)
        self.assertEqual(vp.camera_pos, (17, 31))

    def test__move_camera__east_loops(self):
        vp = make_viewport()
        vp.camera_pos = (31, 0)
        vp.move_camera(CameraDirection.EAST)
        self.assertEqual(vp.camera_pos, (0, 0))
    
    def test__move_camera__west_loops(self):
        vp = make_viewport()
        vp.camera_pos = (0, 0)
        vp.move_camera(CameraDirection.WEST)
        self.assertEqual(vp.camera_pos, (31, 0))
    
if __name__ == "__main__":
    unittest.main()
