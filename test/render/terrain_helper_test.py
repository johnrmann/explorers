import unittest

from unittest.mock import patch

from src.render.utils import height_offset_tile
from src.rendermath.tile import tile_polygon
from src.world.terrain import Terrain

from src.render.viewport import Viewport
from src.render.terrain_helper import TerrainHelper, TerrainSurfacer

class MockTileSurfaceCache:
	def tile_surface(self, zoom, ridges=None, light=None):
		return f"tile_surface({zoom}, {ridges}, {light})"



class TerrainSurfacerTest(unittest.TestCase):
	@patch('src.render.terrain_helper.TileSurfaceCache')
	def setUp(self, _MockTileSurfaceCache):
		_MockTileSurfaceCache.return_value = MockTileSurfaceCache()

		self.terrain_surfacer = TerrainSurfacer()
		self.tile_size = 64


	def test__draws__land_visible(self):
		"""
		Test that it draws land if land is visible.
		"""
		result = list(self.terrain_surfacer.draws(land_visible=True))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0], (-0.0, "tile_surface(64, 0, 7)"))


	def test__draws__land_not_visible(self):
		"""
		Test that it doesn't draw land if land isn't visible.
		"""
		result = list(self.terrain_surfacer.draws(land_visible=False))
		self.assertEqual(len(result), 0)


	def test__draws__land_and_water(self):
		"""
		Test that it draws land and water when both are visible.
		"""
		result = list(
			self.terrain_surfacer.draws(
				land_height=8,
				land_visible=True,
				water_height=8
			)
		)
		self.assertEqual(len(result), 2)
		self.assertEqual(
			result[0], (-32, "tile_surface(64, 0, 7)")
		)
		self.assertEqual(
			result[1], (-64, "tile_surface(64, 0, 7)")
		)


	def test__draws__frozen(self):
		"""
		Test that it draws ice if frozen.
		"""
		result = list(self.terrain_surfacer.draws(is_frozen=True))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0], (-0.0, "tile_surface(64, 0, 7)"))


	def test__draws__ridges(self):
		"""
		Test that it draws ridges if specified.
		"""
		result = list(self.terrain_surfacer.draws(ridges=1))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0], (-0.0, "tile_surface(64, 1, 7)"))


class TerrainHelperTest(unittest.TestCase):
	def setUp(self):
		# This world is land-only.
		flat_heightmap = [
			[8, 8, 8, 8],
			[8, 8, 8, 8],
			[8, 8, 8, 8],
			[8, 8, 8, 8],
		]
		self.land_only = Terrain(flat_heightmap)

		# This world has an ice cap.
		with_ice__land = [
			[5, 5, 5, 5],
			[4, 4, 4, 4],
			[2, 2, 2, 2],
			[1, 1, 1, 1],
		]
		with_ice__ice = [
			[1, 1, 1, 1],
			[2, 2, 2, 2],
			[1, 1, 1, 1],
			[0, 0, 0, 0],
		]
		self.with_ice = Terrain(with_ice__land, icemap=with_ice__ice)

		prefix = 'src.render.terrain_helper.'
		self.patcher_tile_surface_cache = unittest.mock.patch(
			prefix + 'TileSurfaceCache'
		)
		self.mock_tile_surface_cache = self.patcher_tile_surface_cache.start()
		self.mock_tile_surface_cache = MockTileSurfaceCache()
		self.addCleanup(self.patcher_tile_surface_cache.stop)


	def test__land_visible_at__land_only(self):
		"""
		Land is visible on a land-only map.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		self.assertTrue(terrain_helper.land_visible_at((0, 0)))


	def test__land_visible_at__thick_ice(self):
		"""
		Land shouldn't be visible if ice is surrounded by ice at the same
		height.
		"""
		viewport = Viewport((800, 600), self.with_ice)
		terrain_helper = TerrainHelper(self.with_ice, viewport)
		self.assertFalse(terrain_helper.land_visible_at((0, 0)))


	def test__land_visible_at__thin_ice(self):
		"""
		Check that the land is visible if adjacent ice caps are not tall enough
		to cover it.
		"""
		viewport = Viewport((800, 600), self.with_ice)
		terrain_helper = TerrainHelper(self.with_ice, viewport)
		self.assertTrue(terrain_helper.land_visible_at((2, 2)))


	def test__land_visible_at__thick_ice_edge(self):
		"""
		The bottom edge of the world should always have visible land, since we
		can "see into it."
		"""
		viewport = Viewport((800, 600), self.with_ice)
		terrain_helper = TerrainHelper(self.with_ice, viewport)
		self.assertTrue(terrain_helper.land_visible_at((0, 3)))


	def test__land_visible_at__thin_ice_looped(self):
		"""
		Test that checking adjacent cells works on the looped x-axis.
		"""
		viewport = Viewport((800, 600), self.with_ice)
		terrain_helper = TerrainHelper(self.with_ice, viewport)
		self.assertTrue(terrain_helper.land_visible_at((3, 2)))


	def test__tile_draws__land_only(self):
		"""
		Test that it only does one draw for land-only.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		result = list(terrain_helper.tile_draws((0, 0)))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0][0], (-16, -24))


	def test__tile_draws__x_looped(self):
		"""
		Test that it can handle x-looped coordinates. It's possible to draw the
		same cell twice at different positions if zoomed out enough.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		result = list(terrain_helper.tile_draws((4, 0)))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0][0], (48, 8))


	def test__tile_draws__ice_cap_land_visible(self):
		"""
		Test that it can handle cases where the ice cap isn't thick enough
		to cover adjacent land.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.with_ice, viewport)
		result = list(terrain_helper.tile_draws((2, 2)))
		self.assertEqual(len(result), 2)


	def test__tile_bottom_polygon__valid_tile(self):
		"""
		Test tile_bottom_polygon with a valid tile position.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		tile_p = (1, 1)
		result = terrain_helper.tile_bottom_polygon(tile_p)
		expected = tile_polygon(
			viewport.tile_to_screen_coords(tile_p), viewport.tile_dimensions
		)
		self.assertEqual(result, expected)


	def test__tile_top_polygon__valid_tile(self):
		"""
		Test tile_top_polygon with a valid tile position.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		tile_p = (1, 1)
		result = terrain_helper.tile_top_polygon(tile_p)
		bottom = terrain_helper.tile_bottom_polygon(tile_p)
		expected = height_offset_tile(
			bottom, self.land_only.map[1][1] / 8, viewport
		)
		self.assertEqual(result, expected)


	def test__tile_top_polygon__invalid_tile_y(self):
		"""
		Test tile_top_polygon with an invalid tile position (y out of bounds).
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		tile_p = (1, 5)  # y is out of bounds
		result = terrain_helper.tile_top_polygon(tile_p)
		self.assertIsNone(result)


	def test__tile_top_polygon__x_looped(self):
		"""
		Test tile_top_polygon with an invalid tile position (x out of bounds).
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		tile_p = (5, 1)  # x is out of bounds, but still valid bc loops
		result = terrain_helper.tile_top_polygon(tile_p)
		bottom = terrain_helper.tile_bottom_polygon(tile_p)
		expected = height_offset_tile(
			bottom, self.land_only.map[1][1] / 8, viewport
		)
		self.assertEqual(result, expected)


	def test__tile_at_screen_pos__valid_position(self):
		"""
		Test tile_at_screen_pos with a valid screen position.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		screen_p = (400, 300)
		x, y = terrain_helper.tile_at_screen_pos(screen_p)
		expected = (3, 3)  # Expected tile position based on screen coordinates
		self.assertEqual((x, y), expected)


	def test__tile_at_screen_pos__out_of_bounds(self):
		"""
		Test tile_at_screen_pos with a screen position out of bounds.
		"""
		viewport = Viewport((800, 600), self.land_only)
		terrain_helper = TerrainHelper(self.land_only, viewport)
		screen_p = (900, 700)  # out of screen bounds
		result = terrain_helper.tile_at_screen_pos(screen_p)
		self.assertIsNone(result)


if __name__ == "__main__":
	unittest.main()
