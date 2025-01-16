"""
Defines classes for managing the order in which to draw things on the screen.
"""

from src.gameobject.gameobject import GameObject

from src.render.multisurface import MAX_LIGHT_LEVEL_IDX

from src.math.direction import Direction



class RenderTuple:
	"""
	Represents something to draw on the screen.
	"""

	__slots__ = ['cell', 'game_object', 'brightness']

	cell: tuple[int, int]
	game_object: GameObject

	brightness: int

	def __init__(
			self,
			tile: tuple[int, int] = None,
			game_object: GameObject = None,
			brightness: int = MAX_LIGHT_LEVEL_IDX
	):
		"""
		It's recommended that you only set tile XOR game_object.
		"""
		self.cell = tile
		self.game_object = game_object
		self.brightness = brightness



class RenderOrder:
	"""
	An array of RenderTuples that represent the order in which to draw things.
	"""

	_tuples: list[RenderTuple]

	_drawn_cells: set[tuple[int, int]]
	_drawn_game_objects: set[GameObject]

	def __init__(self):
		"""A RenderOrder is initially empty."""
		self._tuples = []
		self._drawn_cells = set()
		self._drawn_game_objects = set()


	def __len__(self):
		"""The length of RenderOrder is the length of the tuples."""
		return len(self._tuples)


	def __iter__(self):
		"""A for loop on RenderOrder will loop through the tuples."""
		return iter(self._tuples)


	def __contains__(self, item):
		"""Returns true if we've already determined how to draw the item."""
		return item in self._drawn_cells or item in self._drawn_game_objects


	def add_cell(self, tile, brightness: int = None):
		"""Marks the tile at the given position as drawn."""
		self._drawn_cells.add(tile)
		self._tuples.append(RenderTuple(tile=tile, brightness=brightness))


	def add_tiles(self, tiles):
		"""Marks the tiles at the given positions as drawn."""
		for tile in tiles:
			self._drawn_cells.add(tile)
			self._tuples.append(RenderTuple(tile=tile))


	def add_game_object(
			self,
			gobj: GameObject,
			camera_orientation: Direction = Direction.NORTHWEST,
			brightness: int = None
	):
		"""Marks the game object, and all cells under it, as drawn."""
		self._drawn_game_objects.add(gobj)
		occupied = gobj.cells_occupied(camera_orientation)
		for occ_cell in occupied:
			if occ_cell not in self._drawn_cells:
				self._tuples.append(
					RenderTuple(tile=occ_cell, brightness=brightness)
				)
				self._drawn_cells.add(occ_cell)
		self._tuples.append(
			RenderTuple(game_object=gobj, brightness=brightness)
		)
