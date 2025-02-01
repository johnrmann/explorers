import unittest

from src.world.biome import Biome

from src.render.colors import (
	BiomeColorScheme,
	DEFAULT_BARREN_COLOR,
	DEFAULT_LUSH_COLOR
)



class BiomeColorSchemeTest(unittest.TestCase):
	def test__init__defaults(self):
		scheme = BiomeColorScheme()
		self.assertEqual(scheme.get_color(Biome.BARREN), DEFAULT_BARREN_COLOR)
		self.assertEqual(scheme.get_color(Biome.LUSH), DEFAULT_LUSH_COLOR)


	def test__init__custom_lush(self):
		scheme = BiomeColorScheme(lush_color=(200, 0, 200))
		self.assertEqual(scheme.get_color(Biome.LUSH), (200, 0, 200))


	def test__init__custom_barren(self):
		scheme = BiomeColorScheme(barren_color=(0, 200, 0))
		self.assertEqual(scheme.get_color(Biome.BARREN), (0, 200, 0))


	def test__get_color__beach(self):
		scheme = BiomeColorScheme()
		self.assertEqual(scheme.get_color(Biome.BEACH), DEFAULT_BARREN_COLOR)


	def test__items(self):
		scheme = BiomeColorScheme()
		for key, color in scheme.items():
			self.assertEqual(scheme.get_color(key), color)



if __name__ == '__main__':
	unittest.main()
