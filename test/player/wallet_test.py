import unittest

from src.player.resources import Resource
from src.player.wallet import Wallet

class WalletTest(unittest.TestCase):
	def test__init__empty(self):
		"""Test that we can create an empty wallet."""
		wallet = Wallet()
		for resource in Resource:
			self.assertEqual(wallet.get(resource), 0)


	def test__init__with_values(self):
		"""Test that we can create a wallet with initial values."""
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: 2,
			Resource.FOOD: 3
		}
		wallet = Wallet(values=values)
		for resource in Resource:
			self.assertEqual(wallet.get(resource), values.get(resource))


	def test__init__maximums_default_infinity(self):
		"""Test that the default maximum is infinity."""
		wallet = Wallet()
		for resource in Resource:
			self.assertEqual(wallet.get_maximum(resource), float('inf'))


	def test__init__maximums(self):
		"""Test that we can set maximums."""
		maximums = {
			Resource.ENERGY: 10,
			Resource.WATER: 20,
			Resource.FOOD: 30
		}
		wallet = Wallet(maximums=maximums)
		for resource in Resource:
			self.assertEqual(wallet.get_maximum(resource), maximums.get(resource))


	def test__init__maximums_value(self):
		"""Test that we can set a single maximum value."""
		maximum = 10
		wallet = Wallet(maximums=maximum)
		for resource in Resource:
			self.assertEqual(wallet.get_maximum(resource), maximum)


	def test__set__single(self):
		"""Test that we can set a single resource."""
		wallet = Wallet()
		wallet.set(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 1)


	def test__set__multiple(self):
		"""Test that we can set multiple resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: 2,
			Resource.FOOD: 3
		}
		wallet.set(values=values)
		for resource in Resource:
			self.assertEqual(wallet.get(resource), values.get(resource))


	def test__add__single(self):
		"""Test that we can add a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		wallet.add(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 2)


	def test__add__multiple(self):
		"""Test that we can add multiple resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: 2,
			Resource.FOOD: 3
		}
		wallet.add(values=values)
		for resource in Resource:
			self.assertEqual(wallet.get(resource), values.get(resource))


	def test__add__rejects_negative(self):
		"""Test that we cannot add negative resources."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		with self.assertRaises(ValueError):
			wallet.add(Resource.ENERGY, -1)


	def test__add__rejects_negative_multiple(self):
		"""Test that we cannot add negative resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: -2,
			Resource.FOOD: 3
		}
		with self.assertRaises(ValueError):
			wallet.add(values=values)


	def test__subtract__single(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		result = wallet.subtract(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 0)
		self.assertTrue(result)


	def test__subtracts__rejects_going_negative(self):
		"""Test that we cannot subtract more than we have."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		result = wallet.subtract(Resource.ENERGY, 2)
		self.assertEqual(wallet.get(Resource.ENERGY), 1)
		self.assertFalse(result)


	def test__subtract__multiple(self):
		"""Test that we can subtract multiple resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 10,
			Resource.WATER: 20,
			Resource.FOOD: 30
		}
		wallet.set(values=values)
		result = wallet.subtract(values={
			Resource.ENERGY: 0,
			Resource.WATER: 10,
			Resource.FOOD: 20
		})
		for resource in Resource:
			self.assertEqual(wallet.get(resource), 10)
		self.assertTrue(result)



if __name__ == '__main__':
	unittest.main()
