import unittest

from src.gen.terrain_generator import TerrainGenerator

class TerrainGeneratorTest(unittest.TestCase):
	def test__init__default(self):
		tgen = TerrainGenerator()
		self.assertEqual(tgen.width, 256)
		self.assertEqual(tgen.height, 128)
		self.assertEqual(tgen.dimensions, (256, 128))


	def test__init__sets_values(self):
		tgen = TerrainGenerator(64, 32, avg_cell_area=4)
		self.assertEqual(tgen.width, 64)
		self.assertEqual(tgen.height, 32)
		self.assertEqual(tgen.dimensions, (64, 32))


	def test__set_ice_caps(self):
		tgen = TerrainGenerator(64, 32, avg_cell_area=4)
		tgen.set_ice_caps()
		terrain = tgen.make()
		ice_area = terrain.ice_area
		self.assertGreaterEqual(ice_area, 64 + 64)


	def test__make__no_water_or_ice(self):
		tgen = TerrainGenerator(64, 32, avg_cell_area=4)
		tgen.set_landmasses()
		terrain = tgen.make()
		self.assertEqual(terrain.land_area, 64 * 32)
		self.assertEqual(terrain.ice_area, 0)
		self.assertEqual(terrain.water_area, 0)


	def test__make__ocean_no_ice(self):
		tgen = TerrainGenerator(64, 32, avg_cell_area=4)
		tgen.set_landmasses()
		tgen.set_ocean()
		terrain = tgen.make()
		self.assertLess(terrain.land_area, 64 * 32)
		self.assertEqual(terrain.ice_area, 0)
		self.assertLess(terrain.water_area, 64 * 32)
		self.assertEqual(terrain.land_area + terrain.water_area, 64 * 32)


if __name__ == "__main__":
	unittest.main()
