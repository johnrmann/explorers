import unittest
import random

from src.world.atmosphere import (
	Atmosphere,
	AtmosphereElement
)

from src.gen.atmosphere_generator import (
	generate_atmosphere,
	AtmosphereType
)

class TestAtmosphereGenerator(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# Set the random seed for deterministic results.
		random.seed(42)  

	def test__generate_atmosphere__earth_like__pressure(self):
		atmosphere = generate_atmosphere(AtmosphereType.EARTH_LIKE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(atmosphere.density(), 1.0, delta=0.1)

	def test__generate_atmosphere__earth_like__composition(self):
		atmosphere = generate_atmosphere(AtmosphereType.EARTH_LIKE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.OXYGEN], 0.207, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.NITROGEN], 0.789, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.CARBON], 0.001, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.WATER], 0.001, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.METHANE], 0.001, places=3
		)

	def test__generate_atmosphere__mars_like__pressure(self):
		atmosphere = generate_atmosphere(AtmosphereType.MARS_LIKE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertTrue(0.01 <= atmosphere.density() <= 0.10)

	def test__generate_atmosphere__mars_like__composition(self):
		atmosphere = generate_atmosphere(AtmosphereType.MARS_LIKE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.CARBON], 1.0, places=3
		)

	def test__generate_atmosphere__hothouse__pressure(self):
		atmosphere = generate_atmosphere(AtmosphereType.HOTHOUSE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(atmosphere.density(), 2.0, delta=0.5)

	def test__generate_atmosphere__hothouse__composition(self):
		atmosphere = generate_atmosphere(AtmosphereType.HOTHOUSE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.CARBON], 1.0, places=3
		)

	def test__generate_atmosphere__titan_like__pressure(self):
		atmosphere = generate_atmosphere(AtmosphereType.TITAN_LIKE)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(atmosphere.density(), 1.5, delta=0.375)

	def test__generate_atmosphere__proto_earth__pressure(self):
		atmosphere = generate_atmosphere(AtmosphereType.PROTO_EARTH)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(atmosphere.density(), 0.75, delta=0.3)

	def test__generate_atmosphere__proto_earth__composition(self):
		atmosphere = generate_atmosphere(AtmosphereType.PROTO_EARTH)
		self.assertIsInstance(atmosphere, Atmosphere)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.OXYGEN], 0.005, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.NITROGEN], 0.3156, places=3
		)
		self.assertAlmostEqual(
			atmosphere.composition[AtmosphereElement.CARBON], 0.679, places=3
		)

	def test__generate_atmosphere__invalid_type(self):
		with self.assertRaises(ValueError):
			generate_atmosphere(AtmosphereType(100))

if __name__ == '__main__':
	unittest.main()
