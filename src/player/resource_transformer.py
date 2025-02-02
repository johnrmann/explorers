from src.mgmt.tick import Tickable

from src.player.wallet import BaseWallet, SuperWallet
from src.player.resources import Resource



class ResourceTransformer(Tickable):
	"""
	Objects of this class transform one resource to another.
	"""

	_source: SuperWallet
	_dest: SuperWallet

	inputs: dict[Resource, int]
	outputs: dict[Resource, int]

	period: int
	_progress: int

	def __init__(
			self,
			inputs: dict[Resource, int] = None,
			outputs: dict[Resource, int] = None,
			period: int = 1
	):
		if inputs is None:
			inputs = {}
		if outputs is None:
			outputs = {}
		self.inputs = inputs
		self.outputs = outputs
		self.period = period
		self._progress = 0
		self._source = SuperWallet()
		self._dest = SuperWallet()


	def add_source(self, wallet: BaseWallet):
		"""
		Add a source wallet.
		"""
		self._source.add_wallet(wallet)


	def add_dest(self, wallet: BaseWallet):
		"""
		Add a destination wallet.
		"""
		self._dest.add_wallet(wallet)


	def remove_source(self, wallet: BaseWallet):
		"""
		Remove a source wallet.
		"""
		self._source.remove_wallet(wallet)


	def remove_dest(self, wallet: BaseWallet):
		"""
		Remove a destination wallet.
		"""
		self._dest.remove_wallet(wallet)


	def is_wired(self):
		"""
		Return true if there is at least one source and one destination.
		"""
		return not self._source.is_empty() and not self._dest.is_empty()


	def transform(self):
		"""
		Attempt to transform the resources.
		"""
		if not self.is_wired():
			return False
		can_do = True
		for resource, value in self.inputs.items():
			if self._source.get(resource) < value:
				can_do = False
				break
		for resource, value in self.outputs.items():
			if self._dest.capacity(resource) < value:
				can_do = False
				break
		if can_do:
			for resource, value in self.inputs.items():
				self._source.subtract(resource, value)
			for resource, value in self.outputs.items():
				self._dest.add(resource, value)
		return can_do


	def tick(self, dt: float, utc: float):
		"""Do nothing."""
		pass


	def tick_second(self, dt: float, utc: float):
		"""Do nothing."""
		if self.period == 0:
			return
		self._progress += dt
		self._progress = int(self._progress)
		if self._progress >= self.period:
			n_transforms = self._progress // self.period
			self._progress = self._progress % self.period
			for _ in range(n_transforms):
				self.transform()
