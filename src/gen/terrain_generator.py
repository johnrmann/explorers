import numpy as np
import noise
import random

from ..world.terrain import Terrain
from src.math.voronoi import make_voronoi
from src.math.adj import select_adj_degree, bool_adj_from_labels

TERRAIN_X = 128
TERRAIN_Y = TERRAIN_X // 2
TERRAIN_Z = TERRAIN_Y // 2

LANDING_SIDE_LENGTH = 32

SCALE = 20

class TerrainGenerator(object):
	def __init__(self, width = TERRAIN_X, height = TERRAIN_Y):
		self.terrain = np.zeros((height, width))
		self._voronoi()
	
	def _voronoi(self, avg_area = 25):
		h = len(self.terrain)
		w = len(self.terrain[0])
		n_points = (w * h) // avg_area
		points_raw = np.random.rand(n_points, 2)
		points = [
			(int(x * w), int(y * h)) for x,y in points_raw
		]
		voronoi = make_voronoi((w,h), points)
		v_adj = bool_adj_from_labels(voronoi, n_points)

		remaining = set(range(n_points))
		while len(remaining) != 0:
			p = random.choice(list(remaining))
			remaining.remove(p)
			to_set_land = select_adj_degree(v_adj, p, degree=2)
			for land_label in to_set_land:
				self._set_height(voronoi, land_label, 10)
			to_set_sea = select_adj_degree(v_adj, p, degree=4) - to_set_land
			for sea_label in to_set_sea:
				self._set_height(voronoi, sea_label, 2)
			remaining -= to_set_sea | to_set_land
	
	def _set_height(self, voronoi, label, h):
		for y in range(len(self.terrain)):
			for x in range(len(self.terrain[0])):
				if voronoi[y][x] == label:
					self.terrain[y][x] = h
	
	def make_landing_area(self):
		width = len(self.terrain[0])
		height = len(self.terrain)
		y = height // 2
		x = width // 2
		s = LANDING_SIDE_LENGTH // 2
		z = self.terrain[y][x]
		for dx in range(x-s,x+s):
			for dy in range(y-s,y+s):
				self.terrain[dy][dx] = z
	
	def make(self):
		return Terrain(self.terrain)
