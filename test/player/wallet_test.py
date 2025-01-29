import unittest

from src.player.resources import Resource
from src.player.wallet import Wallet, SuperWallet

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


	def test__init__maximums_default_zero(self):
		"""Test that the default maximum is infinity."""
		wallet = Wallet()
		for resource in Resource:
			self.assertEqual(wallet.get_maximum(resource), 0)


	def test__init__maximums_default_values(self):
		"""Test that maximums use values as default if present."""
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: 2,
			Resource.FOOD: 3
		}
		wallet = Wallet(values=values)
		for resource in Resource:
			self.assertEqual(wallet.get_maximum(resource), values.get(resource))


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


	def test__get_values(self):
		"""Test that we can get the values."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		self.assertEqual(wallet.values, {Resource.ENERGY: 1})


	def test__get_maximums(self):
		"""Test that we can get the maximums."""
		wallet = Wallet(maximums={Resource.ENERGY: 10})
		self.assertEqual(wallet.maximums, {Resource.ENERGY: 10})


	def test__join_two_wallets(self):
		"""Test that we can join two wallets together."""
		wallet1 = Wallet(values={Resource.ENERGY: 1})
		wallet2 = Wallet(values={Resource.ENERGY: 2})
		result = wallet1 | wallet2
		self.assertEqual(result.get(Resource.ENERGY), 3)


	def test__join_wallet_to_non_wallet(self):
		"""Test that we cannot join a wallet to a non-wallet."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		with self.assertRaises(ValueError):
			wallet | 1


	def test__join_two_wallets_maximums(self):
		"""Test that we can join two wallets together with maximums."""
		wallet1 = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		wallet2 = Wallet(
			values={Resource.ENERGY: 2},
			maximums={Resource.ENERGY: 10}
		)
		result = wallet1 | wallet2
		self.assertEqual(result.get(Resource.ENERGY), 3)
		self.assertEqual(result.get_maximum(Resource.ENERGY), 20)


	def test__capacity(self):
		"""Test that we can get the capacity of a resource."""
		wallet = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		self.assertEqual(wallet.capacity(Resource.ENERGY), 9)


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
		wallet = Wallet(values={Resource.ENERGY: 1}, maximums=99)
		overflow = wallet.add(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 2)
		self.assertEqual(overflow, 0)


	def test__add__single_overflow(self):
		"""Test that if we go over capacity, the overflow is returned to us."""
		wallet = Wallet(
			values={Resource.ENERGY: 9},
			maximums={Resource.ENERGY: 10}
		)
		overflow = wallet.add(Resource.ENERGY, 2)
		self.assertEqual(wallet.get(Resource.ENERGY), 10)
		self.assertEqual(overflow, 1)


	def test__add__multiple(self):
		"""Test that we can add multiple resources."""
		wallet = Wallet(maximums=999)
		values = {
			Resource.ENERGY: 1,
			Resource.WATER: 2,
			Resource.FOOD: 3
		}
		overflow = wallet.add(values=values)
		self.assertEqual(overflow, {})
		for resource in Resource:
			self.assertEqual(wallet.get(resource), values.get(resource))


	def test__add__multiple_overflow(self):
		"""Test that we can add multiple resources with overflow."""
		wallet = Wallet(
			values={Resource.ENERGY: 9},
			maximums=10
		)
		values = {
			Resource.ENERGY: 2,
			Resource.WATER: 3,
			Resource.FOOD: 4
		}
		overflow = wallet.add(values=values)
		self.assertEqual(wallet.get(Resource.ENERGY), 10)
		self.assertEqual(overflow, {Resource.ENERGY: 1})


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


	def test__subtract__rejects_negative(self):
		"""Test that we cannot subtract negative resources."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		with self.assertRaises(ValueError):
			wallet.subtract(Resource.ENERGY, -1)


	def test__subtract__single(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		wallet.subtract(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 0)


	def test__subtract__overflow(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		overflow = wallet.subtract(Resource.ENERGY, 2)
		self.assertEqual(wallet.get(Resource.ENERGY), 0)
		self.assertEqual(overflow, 1)


	def test__subtract__multiple(self):
		"""Test that we can subtract multiple resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 10,
			Resource.WATER: 20,
			Resource.FOOD: 30
		}
		wallet.set(values=values)
		wallet.subtract(values={
			Resource.ENERGY: 0,
			Resource.WATER: 10,
			Resource.FOOD: 20
		})
		self.assertEqual(wallet.get(Resource.ENERGY), 10)
		self.assertEqual(wallet.get(Resource.WATER), 10)
		self.assertEqual(wallet.get(Resource.FOOD), 10)


	def test__subtract__multiple_overflow(self):
		"""Test that we can subtract multiple resources with overflow."""
		wallet = Wallet(values={Resource.ENERGY: 10})
		values = {
			Resource.ENERGY: 12,
			Resource.WATER: 3,
			Resource.FOOD: 4
		}
		overflow = wallet.subtract(values=values)
		self.assertEqual(wallet.get(Resource.ENERGY), 0)
		self.assertEqual(overflow, {
			Resource.ENERGY: 2,
			Resource.WATER: 3,
			Resource.FOOD: 4
		})


	def test__safe_subtract__single(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		result = wallet.safe_subtract(Resource.ENERGY, 1)
		self.assertEqual(wallet.get(Resource.ENERGY), 0)
		self.assertTrue(result)


	def test__safe_subtract__rejects_going_negative(self):
		"""Test that we cannot subtract more than we have."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		result = wallet.safe_subtract(Resource.ENERGY, 2)
		self.assertEqual(wallet.get(Resource.ENERGY), 1)
		self.assertFalse(result)


	def test__safe_subtract__multiple(self):
		"""Test that we can subtract multiple resources."""
		wallet = Wallet()
		values = {
			Resource.ENERGY: 10,
			Resource.WATER: 20,
			Resource.FOOD: 30
		}
		wallet.set(values=values)
		result = wallet.safe_subtract(values={
			Resource.ENERGY: 0,
			Resource.WATER: 10,
			Resource.FOOD: 20
		})
		for resource in Resource:
			self.assertEqual(wallet.get(resource), 10)
		self.assertTrue(result)



class SuperWalletTest(unittest.TestCase):
	def test__init__empty(self):
		"""Test that we can create an empty super wallet."""
		wallet = SuperWallet()
		for resource in Resource:
			self.assertEqual(wallet.get(resource), 0)


	def test__init__with_wallets(self):
		"""Test that we can create a super wallet with initial wallets."""
		wallet1 = Wallet(values={Resource.ENERGY: 1})
		wallet2 = Wallet(values={Resource.WATER: 2})
		super_wallet = SuperWallet(wallets={wallet1, wallet2})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 1)
		self.assertEqual(super_wallet.get(Resource.WATER), 2)


	def test__values(self):
		"""Test that we can retrieve a dict of values."""
		wallet1 = Wallet(values={Resource.ENERGY: 1})
		wallet2 = Wallet(values={Resource.WATER: 2})
		super_wallet = SuperWallet(wallets={wallet1, wallet2})
		self.assertEqual(super_wallet.values, {
			Resource.ENERGY: 1,
			Resource.WATER: 2
		})


	def test__maximums(self):
		"""Test that we can retrieve a dict of maximums."""
		wallet1 = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		wallet2 = Wallet(
			values={Resource.WATER: 2},
			maximums={Resource.WATER: 20}
		)
		super_wallet = SuperWallet(wallets={wallet1, wallet2})
		self.assertEqual(super_wallet.maximums, {
			Resource.ENERGY: 10,
			Resource.WATER: 20,
		})
		self.assertEqual(super_wallet.get_maximum(Resource.ENERGY), 10)
		self.assertEqual(super_wallet.get_maximum(Resource.WATER), 20)


	def test__capacity(self):
		"""Test that we can get capacity."""
		wallet1 = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		wallet2 = Wallet(
			values={Resource.ENERGY: 2},
			maximums={Resource.ENERGY: 10}
		)
		super_wallet = SuperWallet(wallets={wallet1, wallet2})
		self.assertEqual(super_wallet.capacity(Resource.ENERGY), 17)


	def test__add_wallet(self):
		"""Test that we can add a wallet to a super wallet."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 1)


	def test__remove_wallet(self):
		"""Test that we can remove a wallet from a super wallet."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.remove_wallet(wallet)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 0)


	def test__add__simple(self):
		"""Test that we can add resources to a wallet inside the super
		wallet."""
		wallet = Wallet(values={Resource.ENERGY: 1}, maximums=999)
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.add(Resource.ENERGY, 1)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 2)


	def test__add__single_overflow(self):
		"""Test overflow of adding a single resource."""
		wallet = Wallet(
			values={Resource.ENERGY: 9},
			maximums={Resource.ENERGY: 10}
		)
		wallet2 = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.add_wallet(wallet2)
		overflow = super_wallet.add(Resource.ENERGY, 2)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 12)
		self.assertEqual(overflow, 0)


	def test__add__overflow__no_capacity(self):
		"""Test overflow when there is no capacity."""
		wallet = Wallet(
			values={Resource.ENERGY: 9},
			maximums={Resource.ENERGY: 10}
		)
		wallet2 = Wallet(
			values={Resource.ENERGY: 1},
			maximums={Resource.ENERGY: 10}
		)
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.add_wallet(wallet2)
		overflow = super_wallet.add(Resource.ENERGY, 11)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 20)
		self.assertEqual(overflow, 1)


	def test__add__multiple(self):
		"""Test that we can add multiple resources to a wallet inside the super
		wallet."""
		wallet = Wallet(values={Resource.ENERGY: 1}, maximums=999)
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.add(values={Resource.ENERGY: 2})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 3)


	def test__add__multiple_overflow(self):
		"""Test overflow of adding multiple resources."""
		wallet = Wallet(
			values={Resource.ENERGY: 9, Resource.WATER: 9},
			maximums={Resource.ENERGY: 10, Resource.WATER: 10}
		)
		wallet2 = Wallet(
			values={Resource.ENERGY: 1, Resource.WATER: 1},
			maximums={Resource.ENERGY: 10, Resource.WATER: 1}
		)
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.add_wallet(wallet2)
		overflow = super_wallet.add(values={
			Resource.ENERGY: 2,
			Resource.WATER: 2
		})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 12)
		self.assertEqual(super_wallet.get(Resource.WATER), 11)
		self.assertEqual(overflow, {Resource.WATER: 1})


	def test__subtract__single(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.subtract(Resource.ENERGY, 1)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 0)


	def test__subtract__single_overflow(self):
		"""Test overflow of subtracting a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		overflow = super_wallet.subtract(Resource.ENERGY, 2)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 0)
		self.assertEqual(overflow, 1)


	def test__subtract__multiple(self):
		"""Test that we can subtract multiple resources."""
		wallet = Wallet(values={Resource.ENERGY: 10})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		super_wallet.subtract(values={Resource.ENERGY: 1})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 9)


	def test__subtract__multiple_overflow(self):
		"""Test overflow of subtracting multiple resources."""
		wallet = Wallet(values={Resource.ENERGY: 10})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		overflow = super_wallet.subtract(values={Resource.ENERGY: 11})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 0)
		self.assertEqual(overflow, {Resource.ENERGY: 1})


	def test__safe_subtract__single(self):
		"""Test that we can subtract a single resource."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		result = super_wallet.safe_subtract(Resource.ENERGY, 1)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 0)
		self.assertTrue(result)


	def test__safe_subtract__rejects_going_negative(self):
		"""Test that we cannot subtract more than we have."""
		wallet = Wallet(values={Resource.ENERGY: 1})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		result = super_wallet.safe_subtract(Resource.ENERGY, 2)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 1)
		self.assertFalse(result)


	def test__safe_subtract__multiple(self):
		"""Test that we can subtract multiple resources."""
		wallet = Wallet(values={Resource.ENERGY: 10})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		result = super_wallet.safe_subtract(values={Resource.ENERGY: 1})
		self.assertTrue(result)
		self.assertEqual(super_wallet.get(Resource.ENERGY), 9)


	def test__safe_subtract__multiple_overflow(self):
		"""Test that we can subtract multiple resources with overflow."""
		wallet = Wallet(values={Resource.ENERGY: 10})
		super_wallet = SuperWallet()
		super_wallet.add_wallet(wallet)
		result = super_wallet.safe_subtract(values={Resource.ENERGY: 11})
		self.assertEqual(super_wallet.get(Resource.ENERGY), 10)
		self.assertFalse(result)



if __name__ == '__main__':
	unittest.main()
