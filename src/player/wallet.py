import math

from collections import defaultdict

from src.player.resources import Resource

class Wallet:
	"""
	A Wallet is a collection of liquid resources that the player can spend.

	Common ways to spend resources include buying items or consumption (eating
	food, using energy).

	Abstraction / notation note - there's a difference between `wallet.add()`
	and `wallet1 | wallet2`. Suppose I have a wallet with $50 in it, and a max
	capacity of $100. Adding something to the wallet is putting more money
	in it. Joining two wallets together is like having two wallets and
	merging them into one. The new wallet has the sum of the two wallets's
	values _and_ maximums.	
	"""

	_values: dict[Resource, int]

	_maximums: dict[Resource, int]

	def __init__(
			self,
			values: dict[Resource, int] = None,
			maximums: int | dict[Resource, int] = None
	):
		self._values = defaultdict(int)
		if values:
			self.set(values=values)
		
		if isinstance(maximums, int):
			self._maximums = defaultdict(lambda: maximums)
		else:
			self._maximums = defaultdict(lambda: math.inf)
			if maximums:
				self._maximums.update(maximums)


	@property
	def values(self) -> dict[Resource, int]:
		return self._values


	@property
	def maximums(self) -> dict[Resource, int]:
		return self._maximums


	def __or__(self, other):
		new_vals = self._values.copy()
		new_maxes = self._maximums.copy()
		if isinstance(other, Wallet):
			for resource, value in other.values.items():
				new_vals[resource] += value
			for resource, value in other.maximums.items():
				new_maxes[resource] += value
			return Wallet(values=new_vals, maximums=new_maxes)
		raise ValueError("Cannot add Wallet to non-Wallet object.")


	def get(self, resource: Resource) -> int:
		return self._values[resource]


	def get_maximum(self, resource: Resource) -> int:
		return self._maximums[resource]


	def capacity(self, resource: Resource) -> int:
		return self._maximums[resource] - self._values[resource]


	def set(
			self,
			resource: Resource = None,
			value: int = None,
			values: dict[Resource, int] = None
	):
		if resource and value:
			self._values[resource] = value
		elif values:
			self._values.update(values)


	def add(
			self,
			resource: Resource = None,
			value: int = None,
			values: dict[Resource, int] = None
	):
		if resource and value:
			if value < 0:
				raise ValueError("Cannot add negative values.")
			self._values[resource] += value
			if self._values[resource] > self._maximums[resource]:
				overflow = self._values[resource] - self._maximums[resource]
				self._values[resource] = self._maximums[resource]
				return overflow
			return 0
		elif values:
			overflow = {}
			for resource, value in values.items():
				if value < 0:
					raise ValueError("Cannot add negative values.")
				this_overflow = self.add(resource, value)
				if this_overflow:
					overflow[resource] = this_overflow
			return overflow


	def _can_subtract(self, resource: Resource, value: int) -> bool:
		return self._values[resource] >= value


	def subtract(
			self,
			resource: Resource = None,
			value: int = None,
			values: dict[Resource, int] = None
	) -> bool:
		if resource and value:
			can_do = self._can_subtract(resource, value)
			if can_do:
				self._values[resource] -= value
			return can_do
		elif values:
			can_do = True
			for resource, value in values.items():
				can_do &= self._can_subtract(resource, value)
			if can_do:
				for resource, value in values.items():
					self._values[resource] -= value
			return can_do
