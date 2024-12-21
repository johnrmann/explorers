import unittest
from unittest.mock import MagicMock
from src.world.history import PlanetHistory
from src.utility.habitability import HabitabilityFactor

class TestPlanetHistory(unittest.TestCase):

	def setUp(self):
		self.mock_world = MagicMock()
		self.mock_world.habitability.return_value = {
			HabitabilityFactor.TOTAL: 0.5,
			HabitabilityFactor.TEMPERATURE: 0.5,
			HabitabilityFactor.PRESSURE: 0.5,
		}
		self.planet_history = PlanetHistory(self.mock_world)

	def test__init(self):
		self.assertEqual(self.planet_history.world, self.mock_world)
		self.assertEqual(
			len(self.planet_history.habitability),
			len(HabitabilityFactor)
		)
		for factor in HabitabilityFactor:
			self.assertEqual(self.planet_history.habitability[factor], [])

	def test__update__habitability_updates_once(self):
		utc = 1234567890.0
		self.planet_history.update(utc)
		for key, value in self.mock_world.habitability().items():
			self.assertEqual(
				self.planet_history.habitability[key],
				[(utc, value)]
			)

	def test__update__habitability_updates_twice(self):
		utc = 1
		self.planet_history.update(utc)
		utc = 2
		self.mock_world.habitability.return_value = {
			HabitabilityFactor.TOTAL: 0.6,
			HabitabilityFactor.TEMPERATURE: 0.6,
			HabitabilityFactor.PRESSURE: 0.6,
		}
		self.planet_history.update(utc)
		for key, _ in self.mock_world.habitability().items():
			self.assertEqual(
				self.planet_history.habitability[key],
				[(1, 0.5), (2, 0.6)]
			)

if __name__ == '__main__':
	unittest.main()
