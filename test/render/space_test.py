import unittest

from src.world.terrain import Terrain

from src.math.direction import Direction

from src.render.viewport import Viewport

class SpaceTest(unittest.TestCase):
	def setUp(self):
		flatland_map = [([1] * 64) for _ in range(64)]
		self.flatland = Terrain(flatland_map)
		self.viewport = Viewport((800,600), self.flatland)
		self.viewport.camera_pos = (0,0)
	
	def test__sanity__tile_size(self):
		self.assertEqual(self.viewport.tile_width, 24)
		self.assertEqual(self.viewport.tile_height, 12)

	def test__tile_to_screen_coords__northwest(self):
		self.viewport.camera_orientation = Direction.NORTHWEST
		self.viewport.camera_pos = (0, 0)
		result1 = self.viewport.tile_to_screen_coords((0, 0))
		self.assertEqual(result1, (400, 300))
		result2 = self.viewport.tile_to_screen_coords((-1, -1))
		self.assertEqual(result2, (400, 300 - 12))

	def test__tile_to_screen_coords__southeast(self):
		self.viewport.camera_orientation = Direction.SOUTHEAST
		self.viewport.camera_pos = (0, 0)
		result = self.viewport.tile_to_screen_coords((1, 1))
		expected_x = 400
		expected_y = 288
		self.assertEqual(result, (expected_x, expected_y))

	def test__screen_to_tile_coords__northwest(self):
		self.viewport.camera_orientation = Direction.NORTHWEST
		self.viewport.camera_pos = (0, 0)
		screen_coords = (400, 300)
		result = self.viewport.screen_to_tile_coords(screen_coords)
		self.assertEqual(result, (0, 0))

	def test__screen_to_tile_coords_southwest(self):
		self.viewport.camera_orientation = Direction.SOUTHWEST
		self.viewport.camera_pos = (0, 0)
		screen_coords = (400, 300)
		result = self.viewport.screen_to_tile_coords(screen_coords)
		self.assertEqual(result, (0, 0))

	def test__screen_to_tile_coords__round_trip(self):
		self.viewport.camera_orientation = Direction.NORTHWEST
		tile_coords = (3, 3)
		screen_coords = self.viewport.tile_to_screen_coords(tile_coords)
		result = self.viewport.screen_to_tile_coords(screen_coords)
		self.assertEqual(result, tile_coords)

if __name__ == "__main__":
	unittest.main()
