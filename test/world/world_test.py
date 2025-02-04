import unittest

from unittest.mock import MagicMock, Mock

from src.utility.habitability import HabitabilityFactor

from src.world.world import World
from src.world.terrain import Terrain
from src.world.horology import Horology
from src.world.astronomy import Astronomy
from src.world.atmosphere import AtmosphereElement, Atmosphere

HMAP = [
	[1, 1, 1],
	[1, 1, 1],
	[1, 1, 1]
]

class TestWorld(unittest.TestCase):

	def test__init(self):
		terrain = Terrain(HMAP)
		horology = Horology()
		astronomy = Astronomy()
		atmosphere_composition = {
			AtmosphereElement.OXYGEN: 21,
			AtmosphereElement.NITROGEN: 78,
			AtmosphereElement.CARBON: 0,
			AtmosphereElement.WATER: 0,
			AtmosphereElement.METHANE: 0,
		}
		world = World(terrain, horology, astronomy, atmosphere_composition)
		self.assertEqual(world.terrain, terrain)
		self.assertEqual(world.horology, horology)
		self.assertEqual(world.astronomy, astronomy)
		self.assertEqual(world.atmosphere.average, atmosphere_composition)


	def test__set_evt_mgr(self):
		terrain = Terrain(HMAP)
		horology = Horology()
		astronomy = Astronomy()
		atmosphere_composition = {
			AtmosphereElement.OXYGEN: 21,
			AtmosphereElement.NITROGEN: 78
		}
		world = World(terrain, horology, astronomy, atmosphere_composition)
		self.assertIsNone(world.evt_mgr)
		evt_mgr = MagicMock()
		evt_mgr.pub = Mock()
		evt_mgr.sub = Mock()
		world.evt_mgr = evt_mgr
		self.assertEqual(world.evt_mgr, evt_mgr)
		self.assertEqual(world.atmosphere.evt_mgr, evt_mgr)


	def test__dimensions__correct_value(self):
		terrain = Terrain(HMAP)
		world = World(terrain)
		self.assertEqual(world.dimensions, terrain.dimensions)


	def test__tick_second__updates_atmosphere(self):
		terrain = Terrain(HMAP)
		world = World(terrain)
		world.game_mgr = MagicMock()
		world.game_mgr.utc = 0
		world.atmosphere.change_delta(AtmosphereElement.OXYGEN, 1)
		world.tick_second(10, 0)
		self.assertEqual(world.atmosphere.total[AtmosphereElement.OXYGEN], 10)


	def test__tick_second__updates_history(self):
		terrain = Terrain(HMAP)
		world = World(terrain)
		world.game_mgr = MagicMock()
		world.game_mgr.utc = 1
		world.atmosphere.change_delta(AtmosphereElement.OXYGEN, 1)
		world.tick_second(1, 0)
		self.assertEqual(
			len(world.history.habitability[HabitabilityFactor.TOTAL]),
			1
		)
		world.game_mgr.utc = 2
		world.tick_second(1, 0)
		self.assertEqual(
			len(world.history.habitability[HabitabilityFactor.TOTAL]),
			2
		)


	def test__tick_second__freezes_water(self):
		terrain = Terrain(HMAP, watermap=HMAP)
		world = World(terrain)
		world.game_mgr = MagicMock()
		world.game_mgr.utc = 0
		world.atmosphere.is_frozen_at = lambda lat: abs(lat - 0.5) < 0.5

		self.assertEqual(world.terrain.water_area, 9)

		world.tick_second(1, 0)
		self.assertEqual(world.terrain.water_area, 6)


	def test__habitability__total1(self):
		terrain = Terrain(HMAP)
		atmosphere = MagicMock(spec=Atmosphere)
		atmosphere.habitability.return_value = {
			HabitabilityFactor.TEMPERATURE: 1,
			HabitabilityFactor.PRESSURE: 1,
		}
		world = World(terrain)
		world.atmosphere = atmosphere
		self.assertEqual(world.habitability(), {
			HabitabilityFactor.TEMPERATURE: 1,
			HabitabilityFactor.PRESSURE: 1,
			HabitabilityFactor.TOTAL: 1,
		})


	def test__habitability__total2(self):
		terrain = Terrain(HMAP)
		atmosphere = MagicMock(spec=Atmosphere)
		atmosphere.habitability.return_value = {
			HabitabilityFactor.TEMPERATURE: 0,
			HabitabilityFactor.PRESSURE: 1,
		}
		world = World(terrain)
		world.atmosphere = atmosphere
		self.assertEqual(world.habitability(), {
			HabitabilityFactor.TEMPERATURE: 0,
			HabitabilityFactor.PRESSURE: 1,
			HabitabilityFactor.TOTAL: 0,
		})


	def test__habitability__total3(self):
		terrain = Terrain(HMAP)
		atmosphere = MagicMock(spec=Atmosphere)
		atmosphere.habitability.return_value = {
			HabitabilityFactor.TEMPERATURE: 0.5,
			HabitabilityFactor.PRESSURE: 0.5,
		}
		world = World(terrain)
		world.atmosphere = atmosphere
		hab = world.habitability()
		self.assertEqual(hab[HabitabilityFactor.TEMPERATURE], 0.5)
		self.assertEqual(hab[HabitabilityFactor.PRESSURE], 0.5)
		self.assertAlmostEqual(hab[HabitabilityFactor.TOTAL], 0.5)



if __name__ == '__main__':
	unittest.main()
