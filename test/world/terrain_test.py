import unittest

from src.world.terrain import Terrain

desert_heightmap = [
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1]
]
desert_watermap = [[0] * 5 for _ in range(5)]

# Note - Waterworld is NOT entirely water. The mountain peaks form some small
# islands of "dry land" (see 'Waterworld' (1994) starring Kevin Costner).
waterworld_heightmap = [
	[0, 0, 0, 0, 0],
	[0, 1, 1, 1, 0],
	[0, 1, 2, 1, 0],
	[0, 1, 1, 1, 0],
	[0, 0, 0, 0, 0],
]
waterworld_watermap = [
	[2, 2, 2, 2, 2],
	[2, 1, 1, 1, 2],
	[2, 1, 0, 1, 2],
	[2, 1, 1, 1, 2],
	[2, 2, 2, 2, 2],
]

surrounded_heightmap = [
	[0, 0, 0, 0, 0, 0],
	[0, 2, 2, 2, 2, 0],
	[0, 0, 0, 0, 0, 0],
]
surrounded_watermap = [
	[1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1],
]

mars_heightmap = desert_heightmap
mars_icemap_shallow = [
	[1] * 5,
	[1] * 5,
	[0] * 5,
	[1] * 5,
	[1] * 5,
]

mars_icemap_deep = [
	[2] * 5,
	[0] * 5,
	[0] * 5,
	[0] * 5,
	[2] * 5,
]

class TerrainTest(unittest.TestCase):
	def test__init__no_water(self):
		terrain = Terrain(desert_heightmap)
		self.assertEqual(terrain.map, desert_heightmap)
		self.assertEqual(terrain.water, desert_watermap)

	def test__init__with_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.map, waterworld_heightmap)
		self.assertEqual(terrain.water, waterworld_watermap)

	def test__height_at__includes_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.height_at((0, 0)), 2)

	def test__land_height_at__no_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.land_height_at((0, 0)), 0)

	def test__land_area__simple(self):
		terrain = Terrain(desert_heightmap)
		self.assertEqual(terrain.land_area, 25)

	def test__land_area__excluding_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.land_area, 1)

	def test__land_area__excluding_ice(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertEqual(terrain.land_area, 5)

	def test__water_area__simple(self):
		terrain = Terrain(desert_heightmap)
		self.assertEqual(terrain.water_area, 0)

	def test__water_area__excluding_land(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.water_area, 24)

	def test__is_valid_coordinates__valid(self):
		terrain = Terrain(desert_heightmap)
		self.assertTrue(terrain.is_valid_coordinates((2, 2)))

	def test__is_valid_coordinates__invalid(self):
		terrain = Terrain(desert_heightmap)
		self.assertFalse(terrain.is_valid_coordinates((2, 5)))

	def test__is_valid_index__valid(self):
		terrain = Terrain(desert_heightmap)
		self.assertTrue(terrain.is_valid_index((2, 2)))

	def test__is_valid_index__invalid(self):
		terrain = Terrain(desert_heightmap)
		self.assertFalse(terrain.is_valid_index((5, 2)))

	def test__coordinates_to_index__wrap_around(self):
		terrain = Terrain(desert_heightmap)
		self.assertEqual(terrain.coordinates_to_index((6, 2)), (1, 2))

	def test__coordinates_to_index__no_wrap(self):
		terrain = Terrain(desert_heightmap)
		self.assertEqual(terrain.coordinates_to_index((2, 2)), (2, 2))

	def test__sea_level__all_land(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		self.assertEqual(terrain.sea_level(), 1)

	def test__sea_level__mostly_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.sea_level(), 2)

	def test__sea_level__real_map(self):
		terrain = Terrain(surrounded_heightmap, surrounded_watermap)
		self.assertEqual(terrain.sea_level(), 1)

	def test__is_cell_land__land(self):
		terrain = Terrain(desert_heightmap)
		self.assertTrue(terrain.is_cell_land((2, 2)))

	def test__is_cell_land__water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertFalse(terrain.is_cell_land((1, 1)))

	def test__is_cell_water__land(self):
		terrain = Terrain(desert_heightmap)
		self.assertFalse(terrain.is_cell_water((2, 2)))

	def test__is_cell_water__water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertTrue(terrain.is_cell_water((1, 1)))

	def test__is_cell_ice__land(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertFalse(terrain.is_cell_ice((2, 2)))

	def test__is_cell_ice__ice(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertTrue(terrain.is_cell_ice((2, 3)))

	def test__is_cell_ice_edge__land(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertFalse(terrain.is_cell_ice_edge((2, 2)))

	def test__is_cell_ice_edge__interior(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertFalse(terrain.is_cell_ice_edge((0, 0)))

	def test__is_cell_ice_edge__edge(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertTrue(terrain.is_cell_ice_edge((0, 1)))

	def test__melt_ice_cell__land(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		melted = terrain.melt_ice_cell((2, 2))
		self.assertEqual(melted, None)

	def test__melt_ice_cell__interior(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertEqual(terrain.ice[2][2], 0)
		melted = terrain.melt_ice_cell((0, 0))
		self.assertEqual(melted, None)

	def test__melt_ice_cell__shallow(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_shallow)
		self.assertEqual(terrain.ice[1][0], 1)
		melted = terrain.melt_ice_cell((0, 1))
		self.assertEqual(melted, (0, 1))
		self.assertEqual(terrain.ice[1][0], 0)
		self.assertEqual(terrain.water[1][0], 1)

	def test__melt_ice_cell__deep(self):
		terrain = Terrain(mars_heightmap, icemap=mars_icemap_deep)
		melted = terrain.melt_ice_cell((0, 0))
		self.assertEqual(melted, (0, 1))
		self.assertEqual(terrain.ice[0][0], 1)
		self.assertEqual(terrain.water[1][0], 1)

class BalanceWaterTest(unittest.TestCase):
	def test__is_puddle_valley_at_cell__flat(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		# Sanity check
		self.assertTrue(terrain.is_cell_water((0, 0)))
		# Actual tests
		self.assertFalse(terrain.is_puddle_valley_at_cell((0, 0)))

	def test__is_puddle_valley_at_cell__land(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertFalse(terrain.is_puddle_valley_at_cell((2, 2)))

	def test__is_puddle_valley_at_cell__true(self):
		puddle_valley = [
			[2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2],
			[2, 2, 1, 2, 2],
			[2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2],
		]
		terrain = Terrain(desert_heightmap, puddle_valley)
		self.assertTrue(terrain.is_puddle_valley_at_cell((2, 2)))

	def test__is_puddle_hill_at_cell__flat(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		# Sanity check
		self.assertTrue(terrain.is_cell_water((0, 0)))
		# Actual tests
		self.assertFalse(terrain.is_puddle_hill_at_cell((0, 0)))

	def test__is_puddle_hill_at_cell__land(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertFalse(terrain.is_puddle_hill_at_cell((2, 2)))

	def test__is_puddle_hill_at_cell__true(self):
		puddle_hill = [
			[2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2],
			[2, 2, 3, 2, 2],
			[2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2],
		]
		terrain = Terrain(desert_heightmap, puddle_hill)
		self.assertTrue(terrain.is_puddle_hill_at_cell((2, 2)))

	def test__is_water_cell_balanced__land(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		self.assertTrue(terrain.is_water_cell_balanced((2, 2)))

	def test__is_water_cell_balanced__ocean(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertTrue(terrain.is_water_cell_balanced((1, 1)))

	def test__is_water_cell_balanced__column(self):
		column_with_water = [
			[0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0],
			[0, 1, 9, 1, 0],
			[0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0],
		]
		terrain = Terrain(desert_heightmap, column_with_water)
		self.assertFalse(terrain.is_water_cell_balanced((2, 2)))

	def test__balance_water__balanced_null(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		terrain.balance_water()
		self.assertEqual(terrain.water, desert_watermap)

	def test__balance_water__balanced(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		terrain.balance_water()
		self.assertEqual(terrain.water, waterworld_watermap)

	def test__balance_water__unbalanced_simple(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		terrain.water[2][2] = 2
		terrain.balance_water()
		self.assertEqual(terrain.water[2][2], 0)
		self.assertEqual(terrain.water[1][2], 1)
		self.assertEqual(terrain.water[2][3], 1)

	def test__balance_water__column(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		terrain.water[2][2] = 5
		terrain.balance_water()
		self.assertEqual(terrain.water[2][2], 1)
		self.assertEqual(terrain.water[2][3], 1)
		self.assertEqual(terrain.water[2][1], 1)
		self.assertEqual(terrain.water[1][2], 1)
		self.assertEqual(terrain.water[3][2], 1)

	def test__balance_water__cup(self):
		cup_map_land = [
			[5, 5, 5, 5, 5],
			[5, 1, 1, 1, 5],
			[5, 1, 1, 1, 5],
			[5, 1, 1, 1, 5],
			[5, 5, 5, 5, 5],
		]
		cup_map_water = [
			[0, 0, 00, 0, 0],
			[0, 0, 00, 0, 0],
			[0, 0, 27, 0, 0],
			[0, 0, 00, 0, 0],
			[0, 0, 00, 0, 0],
		]
		terrain = Terrain(cup_map_land, watermap=cup_map_water)
		terrain.balance_water()
		self.assertEqual(terrain.water[2][2], 23)
		for _ in range(10):
			terrain.balance_water()
		for y in range(1, 4):
			for x in range(1, 4):
				self.assertEqual(terrain.water[y][x], 3)

if __name__ == '__main__':
	unittest.main()
