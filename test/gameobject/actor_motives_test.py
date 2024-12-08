import unittest

from src.gameobject.actor_motives import ActorMotive, ActorMotiveVector
from src.gameobject.actor_motives import guess_motive_delta_for_time
from src.gameobject.actor_motives import guess_motive_delta_for_distance

class ActorMotiveVectorTest(unittest.TestCase):
	def test__initial_values(self):
		amv = ActorMotiveVector()
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 0)
		self.assertEqual(amv.get(ActorMotive.ENERGY), 0)
		self.assertEqual(amv.get(ActorMotive.HUNGER), 0)
		self.assertEqual(amv.get(ActorMotive.SANITY), 0)

	def test__initial_value(self):
		amv = ActorMotiveVector(values=100)
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 100)
		self.assertEqual(amv.get(ActorMotive.ENERGY), 100)
		self.assertEqual(amv.get(ActorMotive.HUNGER), 100)
		self.assertEqual(amv.get(ActorMotive.SANITY), 100)

	def test__custom_initial_values(self):
		values = {
			ActorMotive.OXYGEN: 80,
			ActorMotive.ENERGY: 70,
			ActorMotive.HUNGER: 60,
			ActorMotive.SANITY: 50,
		}
		amv = ActorMotiveVector(values)
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 80)
		self.assertEqual(amv.get(ActorMotive.ENERGY), 70)
		self.assertEqual(amv.get(ActorMotive.HUNGER), 60)
		self.assertEqual(amv.get(ActorMotive.SANITY), 50)

	def test__initial_maxs(self):
		amv = ActorMotiveVector()
		self.assertEqual(amv.max(ActorMotive.OXYGEN), float('inf'))
		self.assertEqual(amv.max(ActorMotive.ENERGY), float('inf'))
		self.assertEqual(amv.max(ActorMotive.HUNGER), float('inf'))
		self.assertEqual(amv.max(ActorMotive.SANITY), float('inf'))

	def test__initial_max(self):
		amv = ActorMotiveVector(maxs=100)
		self.assertEqual(amv.max(ActorMotive.OXYGEN), 100)
		self.assertEqual(amv.max(ActorMotive.ENERGY), 100)
		self.assertEqual(amv.max(ActorMotive.HUNGER), 100)
		self.assertEqual(amv.max(ActorMotive.SANITY), 100)

	def test__custom_initial_maxs(self):
		amv = ActorMotiveVector(maxs={
			ActorMotive.OXYGEN: 100,
			ActorMotive.ENERGY: 90,
			ActorMotive.HUNGER: 80,
			ActorMotive.SANITY: 70,
		})
		self.assertEqual(amv.max(ActorMotive.OXYGEN), 100)
		self.assertEqual(amv.max(ActorMotive.ENERGY), 90)
		self.assertEqual(amv.max(ActorMotive.HUNGER), 80)
		self.assertEqual(amv.max(ActorMotive.SANITY), 70)

	def test__set(self):
		amv = ActorMotiveVector()
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 0)
		amv.set(ActorMotive.OXYGEN, 77)
		self.assertEqual(amv.oxygen, 77)

	def test__set_all(self):
		values = {
			ActorMotive.OXYGEN: 80,
			ActorMotive.ENERGY: 70,
			ActorMotive.HUNGER: 60,
			ActorMotive.SANITY: 50,
		}
		amv = ActorMotiveVector(values)
		amv.set_all(100)
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 100)
		self.assertEqual(amv.get(ActorMotive.ENERGY), 100)
		self.assertEqual(amv.get(ActorMotive.HUNGER), 100)
		self.assertEqual(amv.get(ActorMotive.SANITY), 100)

	def test__add(self):
		amv = ActorMotiveVector()
		self.assertEqual(amv.get(ActorMotive.OXYGEN), 0)
		amv.add(ActorMotive.OXYGEN, 10)
		self.assertEqual(amv.oxygen, 10)

	def test__add__respects_max(self):
		amv = ActorMotiveVector(maxs=100)
		amv.add(ActorMotive.OXYGEN, 50)
		self.assertEqual(amv.oxygen, 50)
		amv.add(ActorMotive.OXYGEN, 60)
		self.assertEqual(amv.oxygen, 100)

	def test__properties(self):
		values = {
			ActorMotive.OXYGEN: 80,
			ActorMotive.ENERGY: 70,
			ActorMotive.HUNGER: 60,
			ActorMotive.SANITY: 50,
		}
		amv = ActorMotiveVector(values)
		self.assertEqual(amv.oxygen, 80)
		self.assertEqual(amv.energy, 70)
		self.assertEqual(amv.hunger, 60)
		self.assertEqual(amv.sanity, 50)

	def test__addition(self):
		amv1 = ActorMotiveVector({
			ActorMotive.OXYGEN: 50,
			ActorMotive.ENERGY: 50,
			ActorMotive.HUNGER: 50,
			ActorMotive.SANITY: 50,
		})
		amv2 = ActorMotiveVector({
			ActorMotive.OXYGEN: 10,
			ActorMotive.ENERGY: 20,
			ActorMotive.HUNGER: 30,
			ActorMotive.SANITY: 40,
		})
		amv3 = amv1 + amv2
		self.assertEqual(amv3.get(ActorMotive.OXYGEN), 60)
		self.assertEqual(amv3.get(ActorMotive.ENERGY), 70)
		self.assertEqual(amv3.get(ActorMotive.HUNGER), 80)
		self.assertEqual(amv3.get(ActorMotive.SANITY), 90)

	def test__addition__invalid(self):
		amv = ActorMotiveVector()
		with self.assertRaises(ValueError):
			amv + 10
	
	def test__scalar(self):
		amv = ActorMotiveVector({
			ActorMotive.OXYGEN: 100,
			ActorMotive.ENERGY: 100,
			ActorMotive.HUNGER: 100,
			ActorMotive.SANITY: 100,
		})
		amv2 = amv * 0.5
		self.assertEqual(amv2.oxygen, 50)
		self.assertEqual(amv2.hunger, 50)
		self.assertEqual(amv2.energy, 50)
		self.assertEqual(amv2.sanity, 50)

	def test__is_desperate_for(self):
		amv = ActorMotiveVector({
			ActorMotive.OXYGEN: 15,
			ActorMotive.ENERGY: 5,
			ActorMotive.HUNGER: 25,
			ActorMotive.SANITY: 5,
		})
		self.assertTrue(amv.is_desperate_for(ActorMotive.OXYGEN))
		self.assertFalse(amv.is_desperate_for(ActorMotive.HUNGER))
		self.assertTrue(amv.is_desperate_for(ActorMotive.ENERGY))
		self.assertTrue(amv.is_desperate_for(ActorMotive.SANITY))

	def test__is_dead(self):
		amv_alive = ActorMotiveVector({
			ActorMotive.OXYGEN: 11,
			ActorMotive.ENERGY: 11,
			ActorMotive.HUNGER: 11,
			ActorMotive.SANITY: 11,
		})
		amv_dead_oxygen = ActorMotiveVector({
			ActorMotive.OXYGEN: 0,
			ActorMotive.ENERGY: 11,
			ActorMotive.HUNGER: 11,
			ActorMotive.SANITY: 11,
		})
		amv_dead_hunger = ActorMotiveVector({
			ActorMotive.OXYGEN: 11,
			ActorMotive.ENERGY: 11,
			ActorMotive.HUNGER: 0,
			ActorMotive.SANITY: 11,
		})
		self.assertFalse(amv_alive.is_dead())
		self.assertTrue(amv_dead_oxygen.is_dead())
		self.assertTrue(amv_dead_hunger.is_dead())

	def test__mutate(self):
		amv1 = ActorMotiveVector({
			ActorMotive.OXYGEN: 50,
			ActorMotive.ENERGY: 50,
			ActorMotive.HUNGER: 50,
			ActorMotive.SANITY: 50,
		})
		amv2 = ActorMotiveVector({
			ActorMotive.OXYGEN: 10,
			ActorMotive.ENERGY: 20,
			ActorMotive.HUNGER: 30,
			ActorMotive.SANITY: 40,
		})
		amv1.mutate(amv2)
		self.assertEqual(amv1.get(ActorMotive.OXYGEN), 60)
		self.assertEqual(amv1.get(ActorMotive.ENERGY), 70)
		self.assertEqual(amv1.get(ActorMotive.HUNGER), 80)
		self.assertEqual(amv1.get(ActorMotive.SANITY), 90)

	def test__mutate__invalid(self):
		amv = ActorMotiveVector()
		with self.assertRaises(ValueError):
			amv.mutate(10)

class TestGuessMotiveDeltaForTime(unittest.TestCase):
	def test__guess_motive_delta_for_time(self):
		dt = 10
		expected_deltas = {
			ActorMotive.OXYGEN: -1,
			ActorMotive.ENERGY: -(1 / 2),
			ActorMotive.HUNGER: -(1 / 4),
			ActorMotive.SANITY: -(1 / 8),
		}
		actual_deltas = guess_motive_delta_for_time(dt)
		self.assertEqual(actual_deltas, expected_deltas)

	def test__guess_motive_delta_for_time__zero(self):
		dt = 0
		expected_deltas = {
			ActorMotive.OXYGEN: 0,
			ActorMotive.ENERGY: 0,
			ActorMotive.HUNGER: 0,
			ActorMotive.SANITY: 0,
		}
		actual_deltas = guess_motive_delta_for_time(dt)
		self.assertEqual(actual_deltas, expected_deltas)

	def test__guess_motive_delta_for_time__negative(self):
		with self.assertRaises(ValueError):
			guess_motive_delta_for_time(-1)

class TestGuessMotiveDeltaForDistance(unittest.TestCase):
	def test__guess_motive_delta_for_distance(self):
		distance = 100  # meters
		speed = 10  # meters per second
		expected_deltas = {
			ActorMotive.OXYGEN: -11,
			ActorMotive.ENERGY: -5.5,
			ActorMotive.HUNGER: -2.75,
			ActorMotive.SANITY: 9.875,
		}
		actual_deltas = guess_motive_delta_for_distance(distance, speed)
		self.assertEqual(
			actual_deltas.get(ActorMotive.OXYGEN),
			expected_deltas[ActorMotive.OXYGEN]
		)
		self.assertEqual(
			actual_deltas.get(ActorMotive.ENERGY),
			expected_deltas[ActorMotive.ENERGY]
		)
		self.assertEqual(
			actual_deltas.get(ActorMotive.HUNGER),
			expected_deltas[ActorMotive.HUNGER]
		)
		self.assertEqual(
			actual_deltas.get(ActorMotive.SANITY),
			expected_deltas[ActorMotive.SANITY]
		)

	def test__guess_motive_delta_for_distance__zero_speed(self):
		distance = 100
		speed = 0
		with self.assertRaises(ValueError):
			guess_motive_delta_for_distance(distance, speed)

	def test__guess_motive_delta_for_distance__negative_distance(self):
		with self.assertRaises(ValueError):
			guess_motive_delta_for_distance(distance=-1, speed=1)

	def test__guess_motive_delta_for_distance__negative_speed(self):
		with self.assertRaises(ValueError):
			guess_motive_delta_for_distance(distance=1, speed=-1)

if __name__ == '__main__':
	unittest.main()