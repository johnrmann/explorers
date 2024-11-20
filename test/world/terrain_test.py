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

	def test__sea_level__all_land(self):
		terrain = Terrain(desert_heightmap, desert_watermap)
		self.assertEqual(terrain.sea_level(), 1)

	def test__sea_level__mostly_water(self):
		terrain = Terrain(waterworld_heightmap, waterworld_watermap)
		self.assertEqual(terrain.sea_level(), 2)

	def test__sea_level__real_map(self):
		terrain = Terrain(surrounded_heightmap, surrounded_watermap)
		self.assertEqual(terrain.sea_level(), 1)

if __name__ == '__main__':
	unittest.main()
