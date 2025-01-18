import numpy as np
import random

from collections import defaultdict

from src.world.terrain import Terrain
from src.math.voronoi import make_voronoi
from src.math.adj import select_adj_degree, bool_adj_from_labels
from src.math.matrix import smooth_matrix, round_matrix_to_int

TERRAIN_X = 256
TERRAIN_Y = TERRAIN_X // 2
TERRAIN_Z = 256

LANDING_SIDE_LENGTH = 32

SCALE = 20

SEABED_HEIGHT = 2
LAND_HEIGHT = 10

class TerrainGenerator:
	"""
	Generate terrain with voronoi cells.
	"""

	_ice_caps = False
	_ice_cap_span = 0
	_ice_cap_thickness = 0
	_ice_cap_buffer = 0

	_landmass_span = 0
	_landmass_thickness = 0
	_landmass_buffer = 0

	_ocean = False
	_sea_level = 0

	def __init__(self, width = None, height = None, avg_cell_area = 64):
		if width is None:
			width = TERRAIN_X
		if height is None:
			height = TERRAIN_Y

		self.width = width
		self.height = height
		self.dimensions = (width, height)

		self.land_map = np.zeros((height, width))
		self.water_map = np.zeros((height, width))
		self.ice_map = np.zeros((height, width))

		self._make_voronoi(avg_area=avg_cell_area)


	def _make_voronoi(self, avg_area = 64):
		n_points = (self.width * self.height) // avg_area
		self.voronoi = make_voronoi(self.dimensions, avg_area)
		self.voronoi_adj = bool_adj_from_labels(self.voronoi, n_points)
		self.voronoi_remaining = set(range(n_points))
		self.land_heights = defaultdict(int)
		self.water_heights = defaultdict(int)
		self.ice_heights = defaultdict(int)
		self.water_cells = set()


	def set_ice_caps(
			self,
			cells_tall = 2,
			ice_thickness = 10,
			cell_buffer = 1
	):
		"""
		Create ice caps at the far north and far south of the map.

		`ice_thickness` is how thick to make the ice, in addition to the sea
		bed.

		`cells_tall` is how many cells tall the ice caps should be. Setting
		`cell_buffer` to a nonzero number ensures that there will always be
		sea bed or ocean between the ice caps and the land.
		"""

		self._ice_caps = True
		self._ice_cap_buffer = cells_tall + cell_buffer
		self._ice_cap_span = cells_tall
		self._ice_cap_thickness = ice_thickness

	def _make_ice_caps(self):
		if not self._ice_caps:
			return

		ice_thickness = self._ice_cap_thickness
		cells_tall = self._ice_cap_span
		buffer_radius = self._ice_cap_buffer
		v_adj = self.voronoi_adj

		to_ice = set()
		to_buffer = set()
		for label in (self.voronoi[0] + self.voronoi[-1]):
			if label not in self.voronoi_remaining:
				continue
			to_ice.add(label)
			to_ice |= select_adj_degree(v_adj, label, degree=cells_tall)
			to_buffer |= select_adj_degree(v_adj, label, degree=buffer_radius)
			self.voronoi_remaining.remove(label)

		to_buffer -= to_ice

		for ice_label in to_ice:
			self.ice_heights[ice_label] = ice_thickness
			self.land_heights[ice_label] = SEABED_HEIGHT
		for buffer_label in to_buffer:
			self.land_heights[buffer_label] = SEABED_HEIGHT
			self.water_cells.add(buffer_label)

		self.voronoi_remaining -= to_ice | to_buffer


	def set_landmasses(
			self,
			cell_radius = 5,
			land_thickness = 10,
			cell_buffer = 2
	):
		"""
		Sets the landmass strategy.

		Use `cell_radius` to use a radius strategy to set landmasses. In this
		case, we will choose a cell at random, and then choose all cells
		adjacent to that cell, then repeat and repeat until we run out of
		radius.

		`cell_buffer` will ensure the minimum distance between landmasses.
		"""

		buffer_radius = cell_radius + cell_buffer
		self._landmass_span = cell_radius - 1
		self._landmass_thickness = land_thickness
		self._landmass_buffer = buffer_radius


	def _make_landmasses(self):
		cell_radius = self._landmass_span
		land_thickness = self._landmass_thickness
		buffer_radius = self._landmass_buffer
		v_adj = self.voronoi_adj
		while self.voronoi_remaining:
			label = random.choice(list(self.voronoi_remaining))
			self.voronoi_remaining.remove(label)
			to_set_land = select_adj_degree(v_adj, label, degree=cell_radius)
			to_set_land &= self.voronoi_remaining
			to_set_land.add(label)
			for land_label in to_set_land:
				self.land_heights[land_label] = land_thickness
			to_set_sea = select_adj_degree(v_adj, label, degree=buffer_radius)
			to_set_sea -= to_set_land
			to_set_sea &= self.voronoi_remaining
			for sea_label in to_set_sea:
				self.land_heights[sea_label] = SEABED_HEIGHT
				self.water_cells.add(sea_label)
			self.voronoi_remaining -= to_set_sea | to_set_land


	def set_ocean(self, sea_level = 6):
		"""
		Make the ocean. `sea_level` is the height of the ocean.
		"""

		self._ocean = True
		self._sea_level = sea_level


	def _make_ocean(self):
		if not self._ocean:
			return
		for y in range(self.height):
			for x in range(self.width):
				label = self.voronoi[y][x]
				if label in self.water_cells:
					self.water_map[y][x] = self._sea_level - self.land_map[y][x]
				else:
					self.water_map[y][x] = 0


	def _apply_height_maps(self):
		for y in range(self.height):
			for x in range(self.width):
				label = self.voronoi[y][x]
				self.land_map[y][x] = self.land_heights[label]
				self.ice_map[y][x] = self.ice_heights[label]
		self.land_map = smooth_matrix(self.land_map)
		self.land_map = round_matrix_to_int(self.land_map)


	def make(self):
		"""
		Create the terrain object.
		"""

		self._make_ice_caps()
		self._make_landmasses()
		self._apply_height_maps()
		self._make_ocean()
		return Terrain(
			self.land_map,
			watermap=self.water_map,
			icemap=self.ice_map
		)
