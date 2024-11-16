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
	lats = []
	longs = []

	def __init__(self, map):
		self.map = map
		w = len(self.map[0])
		h = len(self.map)
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
		return (self.width, self.height)

	@property
	def width(self):
		return len(self.map[0])
	
	@property
	def height(self):
		return len(self.map)

	@property
	def center(self):
		w = len(self.map[0])
		h = len(self.map)
		return Vector2(w // 2, h // 2)

	def is_valid_coordinates(self, p):
		x_valid = 0 <= p.x < self.width
		y_valid = 0 <= p.y < self.height
		return x_valid and y_valid

	def height_at(self, p):
		x, y = p
		return self.map[y][x]
	
	def height_delta(self, p, direction: Direction):
		x, y = p
		dv = direction.value
		return self._height_deltas[y][x][dv]
