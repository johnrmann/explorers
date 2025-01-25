import math

from collections import defaultdict

from src.player.resources import Resource

class Wallet:
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


	def get(self, resource: Resource) -> int:
		return self._values[resource]


	def get_maximum(self, resource: Resource) -> int:
		return self._maximums[resource]


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
		elif values:
			for resource, value in values.items():
				if value < 0:
					raise ValueError("Cannot add negative values.")
				self._values[resource] += value


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
