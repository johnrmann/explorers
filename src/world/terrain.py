from src.math.adj import adj_cells
from src.math.direction import *

def make_height_delta():
	return [0] * 4

class Terrain(object):
	def __init__(self, map):
		self.map = map
		w = len(self.map[0])
		h = len(self.map)
		self._height_deltas = [
			[make_height_delta() for _ in range(w)] for _ in range(h)
		]
		self._calc_height_deltas()
	
	def _calc_height_deltas(self):
		for y in range(self.height):
			for x in range(self.width):
				p = (x,y)
				adjs = adj_cells(self.dimensions, p)
				for i in range(len(adjs)):
					x2,y2 = adjs[i]
					delta = self.map[y][x] - self.map[y2][x2]
					self._height_deltas[y][x][i] = delta

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
		return (w // 2, h // 2)
	
	def lat_long(self, p):
		x,y = p
		cent_x, cent_y = self.center
		dy = cent_y - y
		dx = x - cent_x
		return (dy / self.height, (dx / self.width) * 2)
	
	def height_delta(self, p, direction: Direction):
		x, y = p
		dv = direction.value
		return self._height_deltas[y][x][dv]
