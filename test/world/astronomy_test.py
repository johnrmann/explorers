import unittest

from src.world.astronomy import Astronomy

class AstronomyTest(unittest.TestCase):
	def setUp(self):
		self.earth = Astronomy()
		self.mars = Astronomy(orbital_radius=(142 / 93))

	def test__power_density__earth(self):
		"""
		Earth gets 100% of the raw solar radiation of Earth.
		"""
		self.assertEqual(self.earth.power_density, 1)

	def test__power_density__mars(self):
		"""
		Mars gets 43% of the raw solar radiation of Earth.
		"""
		self.assertAlmostEqual(self.mars.power_density, 0.4289, 4)

if __name__ == '__main__':
	unittest.main()
