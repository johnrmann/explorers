import unittest

from src.world.biome import (
	# Enums
	BiomeTemperature,
	BiomeWetness,
	Biome,
	# Functions
	get_biome_temperature,
	get_biome_wetness,
	get_is_beach,
	get_biome,
	calculate_biomes,
)

CRATER_EAST_LAND = [
	[8, 8, 8, 8, 8],
	[2, 8, 8, 2, 2],
	[2, 8, 8, 2, 1],
	[2, 8, 8, 2, 2],
	[8, 8, 8, 8, 8]
]

CRATER_EAST_WATER = [
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0]
]

class BiomeTest(unittest.TestCase):
	def test__get_biome_temperature(self):
		self.assertEqual(get_biome_temperature(200), BiomeTemperature.BARREN)
		self.assertEqual(get_biome_temperature(100), BiomeTemperature.HOT)
		self.assertEqual(get_biome_temperature(50), BiomeTemperature.TEMPERATE)
		self.assertEqual(get_biome_temperature(0), BiomeTemperature.COLD)
		self.assertEqual(get_biome_temperature(-50), BiomeTemperature.BARREN)


	def test__get_biome_wetness(self):
		self.assertEqual(get_biome_wetness((0, 0)), BiomeWetness.WET)
		self.assertEqual(get_biome_wetness((32, 32)), BiomeWetness.DRY)
		self.assertEqual(get_biome_wetness((-32, -32)), BiomeWetness.BARREN)


	def test__get_is_beach__flat(self):
		self.assertTrue(get_is_beach((3, 0)))
		self.assertTrue(get_is_beach((6, 0)))
		self.assertFalse(get_is_beach((7, 0)))


	def test__get_is_beach__cliff(self):
		self.assertTrue(get_is_beach((1, 3)))
		self.assertFalse(get_is_beach((1, 4)))


	def test__get_is_beach__is_ocean(self):
		self.assertFalse(get_is_beach((0, 0)))


	def test__get_is_beach__no_water(self):
		self.assertFalse(get_is_beach((-1, -1)))


	def test__get_biome__barren(self):
		self.assertEqual(get_biome(-100, (1, 1)), Biome.BARREN)
		self.assertEqual(get_biome(1000, (1, 1)), Biome.BARREN)


	def test__get_biome__ocean(self):
		self.assertEqual(get_biome(50, (0, 0)), Biome.OCEAN)


	def test__get_biome__beach(self):
		self.assertEqual(get_biome(50, (1, 1)), Biome.BEACH)
		self.assertEqual(get_biome(50, (6, 0)), Biome.BEACH)


	def test__get_biome__hot(self):
		self.assertEqual(get_biome(100, (16, 0)), Biome.TROPICAL)
		self.assertEqual(get_biome(100, (256, 0)), Biome.DESERT)


	def test__get_biome__temperate(self):
		self.assertEqual(get_biome(50, (16, 0)), Biome.LUSH)
		self.assertEqual(get_biome(50, (256, 0)), Biome.SAVANNAH)


	def test__get_biome__cold(self):
		self.assertEqual(get_biome(0, (16, 0)), Biome.SNOW)
		self.assertEqual(get_biome(0, (256, 0)), Biome.TUNDRA)


	def test__calculate_biomes__no_land(self):
		with self.assertRaises(ValueError):
			calculate_biomes(
				water_height=[[1]],
				tpr_deg_fs=[1],
			)


	def test__calculate_biomes__no_water(self):
		with self.assertRaises(ValueError):
			calculate_biomes(
				land_height=[[1]],
				tpr_deg_fs=[1],
			)


	def test__calculate_biomes__no_tpr(self):
		with self.assertRaises(ValueError):
			calculate_biomes(
				land_height=[[1]],
				water_height=[[1]],
			)


	def test__calculate_biomes(self):
		land_height = [
			[1] * 24
			for _ in range(24)
		]
		water_height = [
			[0] * 24
			for _ in range(24)
		]
		land_height[0] = [0] * 24
		water_height[0] = [1] * 24
		tprs = [95] * 24
		biomes = calculate_biomes(
			land_height, water_height, tpr_deg_fs=tprs, wet_cutoff=8
		)
		self.assertEqual(biomes[0][0], Biome.OCEAN)
		self.assertEqual(biomes[1][0], Biome.BEACH)
		self.assertEqual(biomes[6][0], Biome.BEACH)
		self.assertEqual(biomes[7][0], Biome.TROPICAL)
		self.assertEqual(biomes[17][0], Biome.DESERT)


	def test__calculate_biomes__kelvin(self):
		land_height = [
			[1] * 24
			for _ in range(24)
		]
		water_height = [
			[0] * 24
			for _ in range(24)
		]
		land_height[0] = [0] * 24
		water_height[0] = [1] * 24
		tprs_dict = {
			idx: 308 for idx in range(24)
		}
		biomes_dict = calculate_biomes(
			land_height, water_height, tpr_kelvins=tprs_dict, wet_cutoff=8
		)
		tprs_list = [308] * 24
		biomes_list = calculate_biomes(
			land_height, water_height, tpr_kelvins=tprs_list, wet_cutoff=8
		)

		self.assertEqual(biomes_dict[0][0], Biome.OCEAN)
		self.assertEqual(biomes_dict[1][0], Biome.BEACH)
		self.assertEqual(biomes_dict[6][0], Biome.BEACH)
		self.assertEqual(biomes_dict[7][0], Biome.TROPICAL)
		self.assertEqual(biomes_dict[17][0], Biome.DESERT)

		self.assertEqual(biomes_list[0][0], Biome.OCEAN)
		self.assertEqual(biomes_list[1][0], Biome.BEACH)
		self.assertEqual(biomes_list[6][0], Biome.BEACH)
		self.assertEqual(biomes_list[7][0], Biome.TROPICAL)
		self.assertEqual(biomes_list[17][0], Biome.DESERT)


	def test__calculate_biomes__loop_x(self):
		tprs = [95] * 5
		biomes = calculate_biomes(
			CRATER_EAST_LAND,
			CRATER_EAST_WATER,
			tpr_deg_fs=tprs,
			wet_cutoff=8,
			loop_x=True
		)
		self.assertEqual(biomes[2][4], Biome.OCEAN)
		self.assertEqual(biomes[2][3], Biome.BEACH)
		self.assertEqual(biomes[2][0], Biome.BEACH)


	def test__calculate_biomes__no_loop_x(self):
		tprs = [95] * 5
		biomes = calculate_biomes(
			CRATER_EAST_LAND,
			CRATER_EAST_WATER,
			tpr_deg_fs=tprs,
			wet_cutoff=8,
			loop_x=False
		)
		self.assertEqual(biomes[2][4], Biome.OCEAN)
		self.assertEqual(biomes[2][3], Biome.BEACH)
		self.assertEqual(biomes[2][0], Biome.DESERT)



if __name__ == '__main__':
	unittest.main()
