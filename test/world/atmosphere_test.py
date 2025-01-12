import unittest

from src.mgmt.event_manager import EventManager

from src.utility.habitability import HabitabilityFactor

from src.world.atmosphere import (
	Atmosphere, AtmosphereElement, EARTH_ATMOSPEHRE_AVG_COMPOSITION,
	greenhouse_factor,
	make_atmosphere_composiiton,
	AtmosphereChangeEvent,
	AtmosphereChangeDeltaEvent,
	AtmosphereChangeTransformEvent,
	compare_atmosphere_dicts,
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
		self.basic = Atmosphere(
			astronomy=Astronomy(),
			average={
				elem: 1000
				for elem in AtmosphereElement
			},
			planet_area=1
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


	def test__init__with_evt_mgr(self):
		evt_mgr = EventManager()
		atm = Atmosphere(
			average=EARTH_ATMOSPEHRE_AVG_COMPOSITION,
			astronomy=Astronomy(),
			evt_mgr=evt_mgr
		)
		self.assertEqual(atm.evt_mgr, evt_mgr)


	def test__string(self):
		"""Test that the atmospheric composition is printed."""
		atm = Atmosphere(
			astronomy=Astronomy(),
			total={
				key: 1000
				for key in AtmosphereElement
			}
		)
		result = str(atm)
		self.assertIn("AtmosphereElement.CARBON - 1000", result)
		self.assertIn("AtmosphereElement.OXYGEN - 1000", result)
		self.assertIn("AtmosphereElement.NITROGEN - 1000", result)
		self.assertIn("AtmosphereElement.METHANE - 1000", result)
		self.assertIn("AtmosphereElement.WATER - 1000", result)


	def test__change_transform__rejects_invalid1(self):
		"""We can't make or use negative amounts of matter."""
		with self.assertRaises(ValueError):
			self.earth.change_transform(
				(AtmosphereElement.CARBON, -100),
				(AtmosphereElement.OXYGEN, 100),
			)


	def test__change_transform__rejects_invalid2(self):
		"""We can't make or use negative amounts of matter."""
		with self.assertRaises(ValueError):
			self.earth.change_transform(
				(AtmosphereElement.CARBON, 100),
				(AtmosphereElement.OXYGEN, -100),
			)


	def test__change_transform__accepts_double_neg(self):
		"""This is for undoing a transformation."""
		self.earth.change_transform(
			(AtmosphereElement.CARBON, -100),
			(AtmosphereElement.OXYGEN, -100),
		)


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


	def test__evolve__identity(self):
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average, {
			elem: 1000
			for elem in AtmosphereElement
		})


	def test__evolve__add(self):
		self.basic.change_delta(AtmosphereElement.CARBON, 100)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 1100)


	def test__evolve__remove(self):
		self.basic.change_delta(AtmosphereElement.CARBON, -100)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 900)


	def test__evolve__remove_cap_zero(self):
		self.basic.change_delta(AtmosphereElement.CARBON, -2000)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 0)


	def test__evolve__transform(self):
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100),
			(AtmosphereElement.OXYGEN, 100),
		)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 900)
		self.assertEqual(self.basic.average[AtmosphereElement.OXYGEN], 1100)


	def test__evolve__transform_multiple(self):
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100),
			(AtmosphereElement.OXYGEN, 100),
		)
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100),
			(AtmosphereElement.OXYGEN, 100),
		)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 800)
		self.assertEqual(self.basic.average[AtmosphereElement.OXYGEN], 1200)


	def test__evolve__transform_undo(self):
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100),
			(AtmosphereElement.OXYGEN, 100),
		)
		self.basic.change_transform(
			(AtmosphereElement.CARBON, -100),
			(AtmosphereElement.OXYGEN, -100),
		)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 1000)
		self.assertEqual(self.basic.average[AtmosphereElement.OXYGEN], 1000)


	def test__evolve__transform_capped(self):
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100),
			(AtmosphereElement.OXYGEN, 100),
		)
		for t in range(20):
			self.basic.tick_second(1, t)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 0)
		self.assertEqual(self.basic.average[AtmosphereElement.OXYGEN], 2000)


	def test__evolve__transform_ratio(self):
		"""
		If there's not enough of the element to complete the reaction, use
		what's available.

		Note in this test we have a special magic reaction where one unit
		of carbon creates two units of oxygen.
		"""
		self.basic.change_transform(
			(AtmosphereElement.CARBON, 100_000),
			(AtmosphereElement.OXYGEN, 200_000),
		)
		self.basic.tick_second(1, 0)
		self.assertEqual(self.basic.average[AtmosphereElement.CARBON], 0)
		self.assertEqual(self.basic.average[AtmosphereElement.OXYGEN], 3000)


	def test__habitability__earth(self):
		hab = self.earth.habitability()
		self.assertAlmostEqual(
			hab[HabitabilityFactor.TEMPERATURE], 0.63625, places=4
		)
		self.assertAlmostEqual(
			hab[HabitabilityFactor.PRESSURE], 1.0, places=4
		)


	def test__delta_tpr_daily(self):
		self.assertEqual(self.earth.delta_tpr_daily(0), 10)
		self.assertEqual(self.earth.delta_tpr_daily(0.25), 0)
		self.assertEqual(self.earth.delta_tpr_daily(0.5), -10)
		self.assertEqual(self.earth.delta_tpr_daily(0.75), 0)


	def test__delta_tpr_latitude(self):
		self.assertEqual(self.earth.delta_tpr_latitude(-1), -15)
		self.assertEqual(self.earth.delta_tpr_latitude(-0.5), 0)
		self.assertEqual(self.earth.delta_tpr_latitude(0), 15)
		self.assertEqual(self.earth.delta_tpr_latitude(0.5), 0)
		self.assertEqual(self.earth.delta_tpr_latitude(1), -15)


	def test__tpr_at__midnight_poles(self):
		self.earth.tpr_surface = lambda: 288
		self.assertEqual(self.earth.tpr_at(0.5, 1), 288 - 15 - 10)


	def test__tpr_at__noon_poles(self):
		self.earth.tpr_surface = lambda: 288
		self.assertEqual(self.earth.tpr_at(0, -1), 288 - 15 + 10)


	def test__tpr_at__noon_equator(self):
		self.earth.tpr_surface = lambda: 288
		self.assertEqual(self.earth.tpr_at(0, 0), 288 + 15 + 10)


	def test__tpr_at__midnight_equator(self):
		self.earth.tpr_surface = lambda: 288
		self.assertEqual(self.earth.tpr_at(0.5, 0), 288 + 15 - 10)


	def test__is_frozen_at__earth_poles_true(self):
		self.earth.tpr_surface = lambda: 275
		self.assertTrue(self.earth.is_frozen_at(1))
		self.assertTrue(self.earth.is_frozen_at(-1))


	def test__is_frozen_at__earth_equator_false(self):
		self.earth.tpr_surface = lambda: 275
		self.assertFalse(self.earth.is_frozen_at(0))


	def test__set_evt_mgr(self):
		"""Test that setting the event manager sets it on the atmosphere."""
		evt_mgr = EventManager()
		self.earth.evt_mgr = evt_mgr
		self.assertIs(self.earth.evt_mgr, evt_mgr)


	def test__set_evt_mgr__final(self):
		"""Test that over-writing the event manager doesnt work."""
		evt_mgr = EventManager()
		self.earth.evt_mgr = evt_mgr
		with self.assertRaises(ValueError):
			self.earth.evt_mgr = evt_mgr


	def test__changes_atmosphere_total_via_event(self):
		evt_mgr = EventManager()
		self.earth.evt_mgr = evt_mgr
		old_carbon = self.earth.total[AtmosphereElement.CARBON]
		evt_mgr.pub(AtmosphereChangeEvent({
			AtmosphereElement.CARBON: 100
		}))
		evt_mgr.tick(0, 0)
		new_carbon = self.earth.total[AtmosphereElement.CARBON]
		self.assertEqual(new_carbon, old_carbon + 100)


	def test__changes_atmosphere_delta_via_event(self):
		evt_mgr = EventManager()
		self.earth.evt_mgr = evt_mgr
		evt_mgr.pub(AtmosphereChangeDeltaEvent({
			AtmosphereElement.CARBON: 100
		}))
		evt_mgr.tick(0, 0)
		new_carbon_delta = self.earth.delta[AtmosphereElement.CARBON]
		self.assertEqual(new_carbon_delta, 100)


	def test__changes_atmosphere_delta_via_event__evolves(self):
		evt_mgr = EventManager()
		self.earth.evt_mgr = evt_mgr
		old_carbon = self.earth.total[AtmosphereElement.CARBON]
		evt_mgr.pub(AtmosphereChangeDeltaEvent({
			AtmosphereElement.CARBON: 100
		}))
		evt_mgr.tick(0, 0)
		self.earth.tick_second(1, 0)
		new_carbon = self.earth.total[AtmosphereElement.CARBON]
		self.assertEqual(new_carbon, old_carbon + 100)
		self.earth.tick_second(1, 0)
		new_carbon = self.earth.total[AtmosphereElement.CARBON]
		self.assertEqual(new_carbon, old_carbon + 200)


	def test__changes_atmosphere_transform_via_event(self):
		evt_mgr = EventManager()
		self.basic.evt_mgr = evt_mgr
		evt_mgr.pub(AtmosphereChangeTransformEvent({
			(AtmosphereElement.CARBON, AtmosphereElement.OXYGEN): (100, 100)
		}))
		evt_mgr.tick(0, 0)
		self.basic.tick_second(1, 0)
		new_carbon = self.basic.total[AtmosphereElement.CARBON]
		self.assertEqual(new_carbon, 900)
		new_oxygen = self.basic.total[AtmosphereElement.OXYGEN]
		self.assertEqual(new_oxygen, 1100)


	def test__atmosphere_change_event__str(self):
		evt = AtmosphereChangeEvent({
			AtmosphereElement.CARBON: 100
		})
		self.assertEqual(
			str(evt),
			"AtmosphereChangeEvent({<AtmosphereElement.CARBON: 2>: 100})"
		)


	def test__atmosphere_change_delta_event__str(self):
		evt = AtmosphereChangeDeltaEvent({
			AtmosphereElement.CARBON: 100
		})
		self.assertEqual(
			str(evt),
			"AtmosphereChangeDeltaEvent({<AtmosphereElement.CARBON: 2>: 100})"
		)


	def test__compare_atmosphere_dicts__same(self):
		a = {}
		b = {}
		self.assertTrue(compare_atmosphere_dicts(a, b))


	def test__compare_atmosphere_dicts__diff(self):
		a = {AtmosphereElement.CARBON: 100}
		b = {}
		self.assertFalse(compare_atmosphere_dicts(a, b))


	def test__compare_atmosphere_dicts__diff2(self):
		a = {AtmosphereElement.CARBON: 100}
		b = {AtmosphereElement.CARBON: 101}
		self.assertFalse(compare_atmosphere_dicts(a, b))


	def test__compare_atmosphere_dicts__same2(self):
		a = {AtmosphereElement.CARBON: 100}
		b = {AtmosphereElement.CARBON: 100}
		self.assertTrue(compare_atmosphere_dicts(a, b))



if __name__ == '__main__':
	unittest.main()
