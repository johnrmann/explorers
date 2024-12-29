import numpy as np

class Visibility:
	"""
	This class manages the concept of visibility and exploration.
	"""

	_dimensions: tuple[int, int]

	_explored: list[list[int]]
	_visible: list[list[int]]

	def __init__(self, dimensions):
		if dimensions is None:
			raise ValueError('Dimensions must be provided')
		if len(dimensions) != 2:
			raise ValueError('Dimensions must be a tuple of two integers')
		self._dimensions = dimensions
		width, height = dimensions
		self._explored = [
			[0 for _ in range(width)]
			for _ in range(height)
		]
		self._visible = [
			[0 for _ in range(width)]
			for _ in range(height)
		]

	def mark_explored(self, position: tuple[int, int], by_player: int):
		"""
		Mark a position as explored by a player.
		"""
		x, y = position
		x %= self._dimensions[0]
		shift = by_player - 1
		mask = 1 << shift
		self._explored[y][x] = self._explored[y][x] | mask

	def is_explored(self, position: tuple[int, int], by_player: int):
		"""
		Is a position explored by a player?
		"""
		x, y = position
		x %= self._dimensions[0]
		mask = 1 << (by_player - 1)
		raw = self._explored[y][x]
		return bool(raw & mask)

	def explored_matrix(self, by_player: int):
		"""
		Return "is_explored" matrix for a player.
		"""
		return [
			[
				(self._explored[y][x] >> (by_player - 1)) & 1
				for x in range(self._dimensions[0])
			]
			for y in range(self._dimensions[1])
		]

	def toggle_visible(self, position: tuple[int, int], by_player: int):
		"""
		Toggles a position's visibility for a player.
		"""
		x, y = position
		x %= self._dimensions[0]
		shift = by_player - 1
		mask = 1 << shift
		self._visible[y][x] ^= mask
		self._explored[y][x] |= mask

	def set_visible(self, position: tuple[int, int], by_player: int):
		"""
		Marks a position as able to be seen by a player.
		"""
		x, y = position
		x %= self._dimensions[0]
		shift = by_player - 1
		mask = 1 << shift
		self._visible[y][x] = self._visible[y][x] | mask
		self._explored[y][x] = self._explored[y][x] | mask

	def set_invisible(self, position: tuple[int, int], by_player: int):
		"""
		Puts a position under the "fog" for a player.
		"""
		x, y = position
		x %= self._dimensions[0]
		shift = by_player - 1
		mask = 1 << shift
		self._visible[y][x] &= ~mask

	def is_visible(self, position: tuple[int, int], by_player: int):
		"""
		Is a position visible to a player?
		"""
		x, y = position
		x %= self._dimensions[0]
		shift = by_player - 1
		raw = self._visible[y][x]
		return bool((raw >> shift) & 1)

	def visible_matrix(self, by_player: int):
		"""
		Return "is_visible" matrix for a player.
		"""
		return [
			[
				(self._visible[y][x] >> (by_player - 1)) & 1
				for x in range(self._dimensions[0])
			]
			for y in range(self._dimensions[1])
		]
