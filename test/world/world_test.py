import unittest

from src.world.world import World
from src.world.terrain import Terrain
from src.world.horology import Horology
from src.world.astronomy import Astronomy
from src.world.atmosphere import AtmosphereElement

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
			AtmosphereElement.NITROGEN: 78
		}
		world = World(terrain, horology, astronomy, atmosphere_composition)
		self.assertEqual(world.terrain, terrain)
		self.assertEqual(world.horology, horology)
		self.assertEqual(world.astronomy, astronomy)
		self.assertEqual(world.atmosphere.average, atmosphere_composition)

	def test__dimensions__correct_value(self):
		terrain = Terrain(HMAP)
		world = World(terrain)
		self.assertEqual(world.dimensions, terrain.dimensions)

	def test__evolve__updates_atmosphere(self):
		terrain = Terrain(HMAP)
		world = World(terrain)
		world.atmosphere.change_delta(AtmosphereElement.OXYGEN, 1)
		world.evolve(d_seconds=10)
		self.assertEqual(world.atmosphere.total[AtmosphereElement.OXYGEN], 10)

if __name__ == '__main__':
	unittest.main()
