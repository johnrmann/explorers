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

	_width: int
	_height: int
	_area: int
	_water_area = 0

	lats = []
	longs = []

	def __init__(self, heightmap: list[list[int]], watermap=None):
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
			self.water = watermap
			self._water_area = sum(
				sum(cell > 0 for cell in row)
				for row in watermap
			)
		self._height_deltas = [
			[make_height_delta() for _ in range(w)] for _ in range(h)
		]
		self._calc_height_deltas()
		self._calc_lat_longs()

	def _calc_height_deltas(self):
		for y in range(self.height):
			for x in range(self.width):
				p = (x,y)
				adjs = adj_cells(self.dimensions, p)
				for i in range(len(adjs)):
					x2,y2 = adjs[i]
					delta = self.map[y][x] - self.map[y2][x2]
					self._height_deltas[y][x][i] = delta

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
		return (self.lats[y], self.longs[x])

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
		return self._area - self._water_area

	@property
	def water_area(self):
		"""The area of the terrain that is water."""
		return self._water_area

	@property
	def center(self):
		"""The intersection of the prime meridian and equator."""
		return Vector2(self._width // 2, self._height // 2)

	def is_valid_coordinates(self, p):
		x_valid = 0 <= p.x < self.width
		y_valid = 0 <= p.y < self.height
		return x_valid and y_valid

	def is_cell_water(self, p):
		"""Is the given cell position water?"""
		x, y = p
		return self.water[y][x] > 0

	def land_height_at(self, p):
		"""Returns the height at the given cell position, ignoring water."""
		x, y = p
		return self.map[y][x]

	def height_at(self, p):
		"""Returns the height at the given cell position, including water."""
		x, y = p
		return self.map[y][x] + self.water[y][x]

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
