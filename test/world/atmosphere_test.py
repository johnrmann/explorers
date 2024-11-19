import unittest

from src.world.atmosphere import (
	Atmosphere, AtmosphereElement, EARTH_ATMOSPEHRE_AVG_COMPOSITION,
	greenhouse_factor,
	make_atmosphere_composiiton,
)
from src.world.astronomy import Astronomy

class AtmosphereTest(unittest.TestCase):
	def setUp(self):
		self.earth = Atmosphere(
			average=EARTH_ATMOSPEHRE_AVG_COMPOSITION,
			astronomy=Astronomy()
		)
		self.mars = Atmosphere(
			astronomy=Astronomy(orbital_radius=(142 / 93)),
			average=make_atmosphere_composiiton({
				AtmosphereElement.CARBON: 1,
			}, 0.02)
		)
		self.venus = Atmosphere(
			astronomy=Astronomy(orbital_radius=(67 / 93)),
			average=make_atmosphere_composiiton({
				AtmosphereElement.CARBON: 1,
			}, 2)
		)

	def test__make_atmosphere_composiiton__earth(self):
		result = make_atmosphere_composiiton(
			EARTH_ATMOSPEHRE_AVG_COMPOSITION, 1
		)
		self.assertEqual(result, EARTH_ATMOSPEHRE_AVG_COMPOSITION)

	def test__greenhouse_factor__earth(self):
		self.assertAlmostEqual(
			greenhouse_factor(EARTH_ATMOSPEHRE_AVG_COMPOSITION),
			1.1294,
			4
		)

	def test__init__with_average(self):
		self.assertEqual(self.earth.average, EARTH_ATMOSPEHRE_AVG_COMPOSITION)

	def test__init__with_total(self):
		total = Atmosphere(
			total={
				key: count * 1000
				for key, count in EARTH_ATMOSPEHRE_AVG_COMPOSITION.items()
			},
			planet_area=1000,
			astronomy=Astronomy()
		)
		self.assertEqual(total.average, EARTH_ATMOSPEHRE_AVG_COMPOSITION)

	def test__init__without_atmosphere_errors(self):
		"""Test that passing neither total nor average raises an error."""
		with self.assertRaises(ValueError):
			Atmosphere(astronomy=Astronomy())

	def test__init__without_astronomy_errors(self):
		"""Test that passing neither total nor average raises an error."""
		with self.assertRaises(ValueError):
			Atmosphere(average=EARTH_ATMOSPEHRE_AVG_COMPOSITION)

	def test__moles_avg__earth(self):
		self.assertEqual(self.earth.moles_avg(), 1000)

	def test__earth__density(self):
		"""Earth's atmosphere is 1/1th as dense as Earth's."""
		self.assertEqual(self.earth.density(), 1.00)

	def test__mars__density(self):
		"""Mars's atmosphere is 1/50th as dense as Earth's."""
		self.assertAlmostEqual(self.mars.density(), 0.02)

	def test__tpr_effective__earth(self):
		self.assertAlmostEqual(self.earth.tpr_effective(), 254.9962, places=4)

	def test__tpr_effective__mars(self):
		self.assertAlmostEqual(self.mars.tpr_effective(), 212.0216, places=2)

	def test__tpr_surface__earth(self):
		self.assertAlmostEqual(self.earth.tpr_surface(), 287.995, places=2)

	def test__tpr_surface__mars(self):
		"""The actual observed average surface temperature of Mars is ~218
		Kelvin. Our model puts it at 218.422. Not bad!"""
		self.assertAlmostEqual(self.mars.tpr_surface(), 218.422, places=2)

	def test__tpr_surface__venus(self):
		"""The actual observed average surface temperature of Venus is ~735
		Kelvin. Our model puts the surface temperature of "Venus" at 742.31.
		"Venus" is in quotes because our Venus has twice the atmospheric
		density of Earth, whereas the real Venus is 50x. This is because we
		don't want Venusian scenarios to be that much harder than Martian
		ones."""
		self.assertAlmostEqual(self.venus.tpr_surface(), 742.31, places=1)

if __name__ == '__main__':
	unittest.main()
