from collections import defaultdict
from src.math.adj import adj_cells
from src.math.direction import *
from src.math.vector2 import Vector2

def make_height_delta():
	return [0] * 4

def lat(y, h):
	center_y = h // 2
	dy = center_y - y
	return dy / h

def long(x, w):
	center_x = w // 2
	dx = x - center_x
	return (dx / w) * 2

class Terrain(object):
	"""
	Represents the terrain of the game world as two heightmaps: one for the
	land layer, and one for the water layer.
	"""

	map: list[list[int]]
	water: list[list[int]]
	ice: list[list[int]]

	_width: int
	_height: int
	_area: int
	_water_area = 0
	_ice_area = 0

	max_tile_height = 0
	min_tile_height = 0

	lats = []
	longs = []

	def __init__(self, heightmap: list[list[int]], watermap=None, icemap=None):
		self.map = heightmap
		w = len(self.map[0])
		h = len(self.map)
		self._width = w
		self._height = h
		self._area = w * h
		if watermap is None:
			self.water = [[0] * w for _ in range(h)]
			self._water_area = 0
		else:
			self.water = [row[:] for row in watermap]
			self._water_area = sum(
				sum(cell > 0 for cell in row)
				for row in watermap
			)
		if icemap is None:
			self.ice = [[0] * w for _ in range(h)]
			self._ice_area = 0
		else:
			self.ice = icemap
			self._ice_area = sum(
				sum(cell > 0 for cell in row)
				for row in icemap
			)
		self._height_deltas = [
			[make_height_delta() for _ in range(w)] for _ in range(h)
		]
		self._calc_height_deltas()
		self._calc_max_min_tile_heights()
		self._calc_lat_longs()

	def _calc_height_deltas(self):
		for y in range(self.height):
			for x in range(self.width):
				p = (x,y)
				adjs = adj_cells(self.dimensions, p)
				for i in range(len(adjs)):
					x2,y2 = adjs[i]
					h1 = self.height_at(p)
					h2 = self.height_at((x2, y2))
					delta = h1 - h2
					self._height_deltas[y][x][i] = delta

	def _calc_max_min_tile_heights(self):
		self.max_tile_height = max(
			max(row) for row in self.map
		)
		self.min_tile_height = min(
			min(row) for row in self.map
		)

	def _calc_lat_longs(self):
		w, h = self.dimensions
		self.lats = [lat(y, h) for y in range(h)]
		self.longs = [long(x, w) for x in range(w)]

	def lat_long(self, p):
		"""
		Returns the latitude and longitude of the given cell position. Note
		that lat is y-axis and long is x-axis.
		"""
		x, y = p
		return (self.lats[y], self.longs[x % self.width])

	@property
	def dimensions(self):
		"""How big is the terrain?"""
		return (self._width, self._height)

	@property
	def width(self):
		"""The width of the terrain in cells."""
		return self._width

	@property
	def height(self):
		"""The height of the terrain in cells."""
		return self._height

	@property
	def area(self):
		"""The total area of the terrain in cells."""
		return self._area

	@property
	def land_area(self):
		"""The area of the terrain that is land."""
		return self._area - self._water_area - self._ice_area

	@property
	def water_area(self):
		"""The area of the terrain that is water."""
		return self._water_area

	@property
	def ice_area(self):
		"""The area of the terrain that is ice."""
		return self._ice_area

	@property
	def center(self):
		"""The intersection of the prime meridian and equator."""
		return Vector2(self._width // 2, self._height // 2)

	def is_valid_coordinates(self, p):
		"""
		Returns true if p = (x, y) are valid cell coordinates.

		Note the difference between a cell's coordinates and a cell's index.
		Cell coordinates are looped about the x-axis, so a cell at (-1, 0) is
		valid coordinates equal to (width - 1, 0), but an invalid index.

		On the other hand, a cell's index is 1:1 with memory positions, so
		(-1, 0) is an invalid index.
		"""
		_, y = p
		return 0 <= y < self.height

	def is_valid_index(self, p):
		"""
		Returns true if p = (x, y) are valid cell indices.

		Note the difference between a cell's coordinates and a cell's index.
		Cell coordinates are looped about the x-axis, so a cell at (-1, 0) is
		valid coordinates equal to (width - 1, 0), but an invalid index.

		On the other hand, a cell's index is 1:1 with memory positions, so
		(-1, 0) is an invalid index.
		"""
		x, y = p
		x_valid = 0 <= x < self.width
		y_valid = 0 <= y < self.height
		return x_valid and y_valid

	def coordinates_to_index(self, p):
		"""
		Converts coordinates to indeces.
		"""
		x, y = p
		return (x % self.width, y)

	def is_cell_land(self, p):
		"""Is the given cell position land?"""
		return not self.is_cell_water(p) and not self.is_cell_ice(p)

	def is_cell_water(self, p):
		"""Is the given cell position water?"""
		x, y = p
		return self.water[y][x % self.width] > 0

	def is_cell_ice(self, p):
		"""Is the given cell position ice?"""
		x, y = p
		return self.ice[y][x % self.width] > 0

	def is_cell_ice_edge(self, p):
		"""Is the given cell position an edge of an ice cap?"""
		x, y = p
		if not self.is_cell_ice(p):
			return False
		for direction in CARDINAL_DIRECTIONS:
			dy, dx = direction_to_delta(direction)
			if not self.is_cell_ice((x + dx, y + dy)):
				return True
		return False

	def land_height_at(self, p):
		"""Returns the height at the given cell position, ignoring water."""
		x, y = p
		return self.map[y][x % self.width]

	def height_at(self, p):
		"""Returns the height at the given cell position, including water."""
		x, y = p
		x_mod = x % self.width
		return self.map[y][x_mod] + self.water[y][x_mod] + self.ice[y][x_mod]

	def height_delta(self, p, direction: Direction):
		x, y = p
		dv = direction.value
		return self._height_deltas[y][x][dv]

	def sea_level(self):
		"""
		Returns the sea level of the terrain. This is used for calculating the
		surface air pressure.
		"""
		height_stogram = [0] * 256 # height histogram
		for y in range(self.height):
			for x in range(self.width):
				land = self.map[y][x]
				water = self.water[y][x]
				height_stogram[land + water] += 1
		height = -1
		max_count = -1
		for i in range(256):
			count = height_stogram[i]
			if count > max_count:
				max_count = count
				height = i
		return height

	def _choose_cell_to_put_melted_ice(self, p):
		"""
		The cell to put melted ice is the cell adjacent to `p` with the lowest
		height.
		"""
		x, y = p
		ret_x, ret_y = -1, -1
		min_h = None
		for direction in CARDINAL_DIRECTIONS:
			dy, dx = direction_to_delta(direction)
			x2, y2 = x + dx, y + dy
			if not self.is_valid_coordinates((x2, y2)):
				continue
			if not min_h or self.height_at((x2, y2)) < min_h:
				min_h = self.height_at((x2, y2))
				ret_x, ret_y = x2, y2
		return ret_x, ret_y

	def melt_ice_cell(self, p):
		"""
		Melts one unit of ice at p and returns the new position of where the
		melt went. If there is no ice at p, or if the ice at p is not at the
		edge, then nothing happens and None is returned.
		"""
		if not self.is_cell_ice(p):
			return None
		if not self.is_cell_ice_edge(p):
			return None
		x, y = p
		if self.ice[y][x] == 1:
			self.ice[y][x] = 0
			self._ice_area -= 1
			self.water[y][x] = 1
			self._water_area += 1
			return p
		else:
			x2, y2 = self._choose_cell_to_put_melted_ice(p)
			self.ice[y][x] -= 1
			if self.water[y2][x2] == 0:
				self._water_area += 1
			self.water[y2][x2] += 1
			return x2, y2

	def is_water_cell_balanced(self, p):
		"""
		Return True if the water cell at the given position is balanced.
		"""
		x, y = p

		# Trivial case: no water to balance.
		if self.water[y][x] == 0:
			return True

		curr_height = self.height_at(p)
		adj = adj_cells(self.dimensions, p)

		# Another trivial case: this height is the same as all the neighbors.
		same_heights = map(
			lambda p2: self.height_at(p2) == curr_height,
			adj
		)
		if all(same_heights):
			return True

		# The trickiest case is the "puddle" case - if this tile is one above
		# its surroundings, then it's a puddle and we can consider it balanced.
		# If it's two or more above, then it's not balanced.
		much_higher = map(
			lambda p2: self.height_at(p2) - curr_height > 1,
			adj
		)
		if any(much_higher):
			return False

		# Water cell is not balanced.
		return False

	def is_puddle_valley_at_cell(self, p):
		"""
		This method returns true if the given cell is a puddle valley.
		"""
		if not self.is_cell_water(p):
			return False
		h = self.height_at(p)
		adj = adj_cells(self.dimensions, p)
		water_adj = filter(self.is_cell_water, adj)
		higher_water_adj = map(
			lambda p2: self.height_at(p2) == h + 1,
			water_adj
		)
		if all(higher_water_adj):
			return True
		return False

	def is_puddle_hill_at_cell(self, p):
		"""
		This method returns true if the given cell is a puddle hill.
		"""
		if not self.is_cell_water(p):
			return False
		h = self.height_at(p)
		adj = adj_cells(self.dimensions, p)
		water_adj = filter(self.is_cell_water, adj)
		lower_water_adj = map(
			lambda p2: self.height_at(p2) == h - 1,
			water_adj
		)
		if all(lower_water_adj):
			return True
		return False

	def _postbalance_water(self):
		"""
		Puddle hill/valleys are artifacts of the water balancing algorithm.
		It's possible for a water cell surrounded by water to be a "puddle
		hill" or "puddle valley", where the difference in height between it and
		its surroundings is one.

		We want to cancel out as many of them as possible to get a flat
		ocean.
		"""
		puddle_hills = set()
		puddle_valleys = set()
		for y in range(self.height):
			for x in range(self.width):
				p = (x, y)
				if self.is_cell_water(p):
					if self.is_puddle_valley_at_cell(p):
						puddle_valleys.add(p)
					elif self.is_puddle_hill_at_cell(p):
						puddle_hills.add(p)
		for valley_p, hill_p in zip(puddle_valleys, puddle_hills):
			vx, vy = valley_p
			hx, hy = hill_p
			self.water[vy][vx] += 1
			self.water[hy][hx] -= 1

	def balance_water(self):
		"""
		Distributes water from higher cells to lower adjacent cells to balance
		the water levels.
		"""
		for y in range(self.height):
			for x in range(self.width):
				if not self.is_cell_water((x, y)):
					continue
				# print("Water at ({}, {})".format(x, y))
				current_height = self.height_at((x, y))
				adj = adj_cells(self.dimensions, (x, y))
				lower_adj = []
				for x2, y2 in adj:
					adj_height = self.height_at((x2, y2))
					diff = current_height - adj_height
					if diff >= 2:
						lower_adj.append(((x2, y2), adj_height))
				if lower_adj and self.water[y][x] > 0:
					# Distribute water to lower neighbors
					lower_adj.sort(key=lambda p: p[1])
					for p2, _ in lower_adj:
						x2, y2 = p2
						if self.is_water_cell_balanced((x, y)):
							break
						self.water[y][x] -= 1
						self.water[y2][x2] += 1
		self._postbalance_water()
