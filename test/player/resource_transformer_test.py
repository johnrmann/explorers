import unittest

from src.player.resources import Resource
from src.player.resource_transformer import ResourceTransformer
from src.player.wallet import SuperWallet, Wallet



class ResourceTransformerTest(unittest.TestCase):
	def setup__water_fuel_transform(self):
		inputs = {Resource.WATER: 10, Resource.ENERGY: 10}
		outputs = {Resource.FUEL: 10}
		src_wallet = Wallet(maximums=1000)
		src_wallet.add(Resource.WATER, 1000)
		src_wallet.add(Resource.ENERGY, 1000)
		dest_wallet = Wallet(maximums=1000)
		rt = ResourceTransformer(inputs, outputs)
		rt.add_source(src_wallet)
		rt.add_dest(dest_wallet)
		return rt, src_wallet, dest_wallet


	def test__init__no_args(self):
		rt = ResourceTransformer()
		self.assertEqual(rt.inputs, {})
		self.assertEqual(rt.outputs, {})


	def test__init__with_args(self):
		inputs = {Resource.WATER: 10, Resource.ENERGY: 10}
		outputs = {Resource.FUEL: 10}
		rt = ResourceTransformer(inputs, outputs)
		self.assertEqual(rt.inputs, inputs)
		self.assertEqual(rt.outputs, outputs)


	def test__init__with_period(self):
		rt = ResourceTransformer(period=10)
		self.assertEqual(rt.period, 10)


	def test__is_wired__init_false(self):
		rt = ResourceTransformer()
		self.assertFalse(rt.is_wired())


	def test__is_wired__false_no_dest(self):
		rt = ResourceTransformer()
		rt.add_source(Wallet())
		self.assertFalse(rt.is_wired())


	def test__is_wired__false_no_source(self):
		rt = ResourceTransformer()
		rt.add_dest(Wallet())
		self.assertFalse(rt.is_wired())


	def test__is_wired__true(self):
		rt = ResourceTransformer()
		rt.add_source(Wallet())
		rt.add_dest(Wallet())
		self.assertTrue(rt.is_wired())


	def test__add_remove_source(self):
		rt = ResourceTransformer()
		src = Wallet()
		dest = Wallet()
		rt.add_source(src)
		rt.add_dest(dest)
		self.assertTrue(rt.is_wired())
		rt.remove_source(src)
		self.assertFalse(rt.is_wired())


	def test__add_remove_dest(self):
		rt = ResourceTransformer()
		src = Wallet()
		dest = Wallet()
		rt.add_source(src)
		rt.add_dest(dest)
		self.assertTrue(rt.is_wired())
		rt.remove_dest(dest)
		self.assertFalse(rt.is_wired())


	def test__transform__not_wired(self):
		rt = ResourceTransformer()
		self.assertFalse(rt.transform())


	def test__transform__works(self):
		src_wallet = Wallet(maximums=1000)
		src_wallet.add(Resource.WATER, 1000)
		src_wallet.add(Resource.ENERGY, 1000)
		dest_wallet = Wallet(maximums=1000)
		rt = ResourceTransformer(
			{Resource.WATER: 10, Resource.ENERGY: 10},
			{Resource.FUEL: 10}
		)
		rt.add_source(src_wallet)
		rt.add_dest(dest_wallet)
		result = rt.transform()
		self.assertTrue(result)
		self.assertEqual(src_wallet.get(Resource.WATER), 990)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 990)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 10)


	def test__transform__not_enough_input(self):
		src_wallet = Wallet(maximums=1000)
		src_wallet.add(Resource.WATER, 5)
		src_wallet.add(Resource.ENERGY, 5)
		dest_wallet = Wallet(maximums=1000)
		rt = ResourceTransformer(
			{Resource.WATER: 10, Resource.ENERGY: 10},
			{Resource.FUEL: 10}
		)
		rt.add_source(src_wallet)
		rt.add_dest(dest_wallet)
		result = rt.transform()
		self.assertFalse(result)
		self.assertEqual(src_wallet.get(Resource.WATER), 5)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 5)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 0)


	def test__transform__not_enough_output(self):
		src_wallet = Wallet(maximums=1000)
		src_wallet.add(Resource.WATER, 1000)
		src_wallet.add(Resource.ENERGY, 1000)
		dest_wallet = Wallet(maximums=1000)
		dest_wallet.add(Resource.FUEL, 1000)
		rt = ResourceTransformer(
			inputs={Resource.WATER: 10, Resource.ENERGY: 10},
			outputs={Resource.FUEL: 5}
		)
		rt.add_source(src_wallet)
		rt.add_dest(dest_wallet)
		result = rt.transform()
		self.assertFalse(result)
		self.assertEqual(src_wallet.get(Resource.WATER), 1000)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 1000)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 1000)


	def test__tick_second__stopped(self):
		"""Recall that period == 0 means that the transformer is stopped."""
		rt, src_wallet, dest_wallet = self.setup__water_fuel_transform()
		rt.period = 0
		rt.tick_second(1, 1)
		self.assertEqual(src_wallet.get(Resource.WATER), 1000)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 1000)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 0)


	def test__tick_second__works(self):
		rt, src_wallet, dest_wallet = self.setup__water_fuel_transform()
		rt.period = 1
		rt.tick_second(1, 1)
		self.assertEqual(src_wallet.get(Resource.WATER), 990)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 990)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 10)


	def test__tick_second__period(self):
		rt, src_wallet, dest_wallet = self.setup__water_fuel_transform()
		rt.period = 3
		rt.tick_second(1, 1)
		self.assertEqual(src_wallet.get(Resource.WATER), 1000)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 1000)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 0)
		rt.tick_second(1, 2)
		self.assertEqual(src_wallet.get(Resource.WATER), 1000)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 1000)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 0)
		rt.tick_second(1, 3)
		self.assertEqual(src_wallet.get(Resource.WATER), 990)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 990)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 10)


	def test__tick_second__overflow(self):
		rt, src_wallet, dest_wallet = self.setup__water_fuel_transform()
		rt.period = 1
		rt.tick_second(3, 3)
		self.assertEqual(src_wallet.get(Resource.WATER), 970)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 970)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 30)


	def test__tick_second__overflow_modulo(self):
		rt, src_wallet, dest_wallet = self.setup__water_fuel_transform()
		rt.period = 10
		rt.tick_second(15, 15)
		self.assertEqual(src_wallet.get(Resource.WATER), 990)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 990)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 10)
		rt.tick_second(4, 19)
		self.assertEqual(src_wallet.get(Resource.WATER), 990)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 990)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 10)
		rt.tick_second(1, 20)
		self.assertEqual(src_wallet.get(Resource.WATER), 980)
		self.assertEqual(src_wallet.get(Resource.ENERGY), 980)
		self.assertEqual(dest_wallet.get(Resource.FUEL), 20)



if __name__ == '__main__':
	unittest.main()
